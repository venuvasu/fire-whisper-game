#!/usr/bin/env python3
"""
Log Manager - Automatically manages gameplay logs
Keeps only the 10 most recent logs and archives older ones with compression
"""
import os
import glob
import gzip
import shutil
import re
from pathlib import Path
from datetime import datetime, timedelta

class LogManager:
    """Manages gameplay logs with automatic cleanup and compression"""
    
    def __init__(self, logs_dir: str = "logs", max_logs: int = 10, archive_logs: bool = True):
        self.logs_dir = Path(logs_dir)
        self.max_logs = max_logs
        self.archive_logs = archive_logs
        self.logs_dir.mkdir(exist_ok=True)
        
        # Create archive directory if archiving is enabled
        if self.archive_logs:
            self.archive_dir = self.logs_dir / "archive"
            self.archive_dir.mkdir(exist_ok=True)
    
    def get_gameplay_logs(self):
        """Get all gameplay log files sorted by creation time (newest first)"""
        log_pattern = str(self.logs_dir / "gameplay_*.txt")
        log_files = glob.glob(log_pattern)
        
        # Sort by modification time (newest first)
        log_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        
        return [Path(f) for f in log_files]
    
    def compress_log_file(self, log_file):
        """Compress a log file using gzip and move to archive directory"""
        try:
            # Create archive filename with same timestamp
            archive_path = self.archive_dir / f"{log_file.stem}.gz"
            
            # Compress the file
            with open(log_file, 'rb') as f_in:
                with gzip.open(archive_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            
            # Get compression stats
            original_size = log_file.stat().st_size
            compressed_size = archive_path.stat().st_size
            compression_ratio = (1 - (compressed_size / original_size)) * 100 if original_size > 0 else 0
            
            return {
                'success': True,
                'original_file': log_file.name,
                'archive_file': archive_path.name,
                'original_size': original_size,
                'compressed_size': compressed_size,
                'compression_ratio': compression_ratio
            }
        except Exception as e:
            print(f"❌ Failed to compress {log_file.name}: {e}")
            return {'success': False, 'error': str(e), 'file': log_file.name}
    
    def cleanup_old_logs(self):
        """Archive or remove old logs, keeping only the most recent max_logs"""
        log_files = self.get_gameplay_logs()
        
        if len(log_files) <= self.max_logs:
            return {
                'cleaned': False,
                'total_logs': len(log_files),
                'removed_count': 0,
                'archived_count': 0,
                'removed_files': [],
                'archived_files': []
            }
        
        # Files to process (everything after max_logs)
        files_to_process = log_files[self.max_logs:]
        removed_files = []
        archived_files = []
        compression_stats = []
        
        for log_file in files_to_process:
            try:
                if self.archive_logs:
                    # Compress and archive
                    result = self.compress_log_file(log_file)
                    if result['success']:
                        archived_files.append(log_file.name)
                        compression_stats.append(result)
                        print(f"📦 Archived log: {log_file.name} → {result['archive_file']} " +
                              f"({result['compression_ratio']:.1f}% reduction)")
                
                # Remove original file
                log_file.unlink()
                removed_files.append(log_file.name)
                if not self.archive_logs:
                    print(f"🗑️  Removed old log: {log_file.name}")
                
            except Exception as e:
                print(f"❌ Failed to process {log_file.name}: {e}")
        
        return {
            'cleaned': True,
            'total_logs': len(log_files),
            'kept_logs': len(log_files) - len(removed_files),
            'removed_count': len(removed_files),
            'archived_count': len(archived_files),
            'removed_files': removed_files,
            'archived_files': archived_files,
            'compression_stats': compression_stats
        }
    
    def get_archived_logs(self):
        """Get all archived log files sorted by creation time (newest first)"""
        if not self.archive_logs or not self.archive_dir.exists():
            return []
            
        archive_pattern = str(self.archive_dir / "gameplay_*.gz")
        archive_files = glob.glob(archive_pattern)
        
        # Sort by modification time (newest first)
        archive_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        
        return [Path(f) for f in archive_files]
    
    def get_log_statistics(self):
        """Get detailed statistics about logs and archives"""
        log_files = self.get_gameplay_logs()
        archive_files = self.get_archived_logs()
        
        # Calculate total sizes
        active_size = sum(f.stat().st_size for f in log_files) if log_files else 0
        archive_size = sum(f.stat().st_size for f in archive_files) if archive_files else 0
        
        # Extract dates from filenames for time range analysis
        date_pattern = re.compile(r'gameplay_(\d{4}-\d{2}-\d{2})_')
        
        active_dates = []
        for log_file in log_files:
            match = date_pattern.search(log_file.name)
            if match:
                active_dates.append(match.group(1))
        
        archive_dates = []
        for archive_file in archive_files:
            match = date_pattern.search(archive_file.name)
            if match:
                archive_dates.append(match.group(1))
        
        # Calculate date ranges
        date_range = {
            'active': {
                'oldest': min(active_dates) if active_dates else None,
                'newest': max(active_dates) if active_dates else None,
            },
            'archive': {
                'oldest': min(archive_dates) if archive_dates else None,
                'newest': max(archive_dates) if archive_dates else None,
            }
        }
        
        # Calculate average compression ratio if archives exist
        compression_ratios = []
        for archive_file in archive_files:
            # Try to find original filename to estimate compression
            original_name = archive_file.stem + '.txt'
            original_path = self.logs_dir / original_name
            
            # If original doesn't exist, estimate based on similar files
            if not original_path.exists() and log_files:
                avg_log_size = active_size / len(log_files)
                compressed_size = archive_file.stat().st_size
                ratio = (1 - (compressed_size / avg_log_size)) * 100
                compression_ratios.append(ratio)
        
        avg_compression = sum(compression_ratios) / len(compression_ratios) if compression_ratios else 0
        
        return {
            'active_logs': {
                'count': len(log_files),
                'total_size': active_size,
                'avg_size': active_size / len(log_files) if log_files else 0
            },
            'archived_logs': {
                'count': len(archive_files),
                'total_size': archive_size,
                'avg_size': archive_size / len(archive_files) if archive_files else 0,
                'avg_compression_ratio': avg_compression
            },
            'date_range': date_range,
            'storage_saved': active_size * (avg_compression / 100) if avg_compression > 0 else 0
        }
    
    def get_log_status(self):
        """Get current status of logs"""
        log_files = self.get_gameplay_logs()
        archive_files = self.get_archived_logs() if self.archive_logs else []
        
        if not log_files:
            return {
                'total_logs': 0,
                'archived_logs': len(archive_files),
                'newest_log': None,
                'oldest_log': None,
                'needs_cleanup': False
            }
        
        newest_log = log_files[0]
        oldest_log = log_files[-1]
        
        return {
            'total_logs': len(log_files),
            'archived_logs': len(archive_files),
            'newest_log': {
                'name': newest_log.name,
                'created': datetime.fromtimestamp(newest_log.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')
            },
            'oldest_log': {
                'name': oldest_log.name,
                'created': datetime.fromtimestamp(oldest_log.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')
            },
            'needs_cleanup': len(log_files) > self.max_logs,
            'logs_to_remove': max(0, len(log_files) - self.max_logs)
        }
    
    def auto_cleanup_on_new_log(self, new_log_path: str):
        """Automatically cleanup when a new log is created"""
        print(f"📝 New log created: {Path(new_log_path).name}")
        
        cleanup_result = self.cleanup_old_logs()
        
        if cleanup_result['cleaned']:
            print(f"🧹 Auto-cleanup: Removed {cleanup_result['removed_count']} old logs")
            print(f"📊 Keeping {cleanup_result['kept_logs']} most recent logs")
        else:
            print(f"📊 Log count: {cleanup_result['total_logs']}/{self.max_logs} (no cleanup needed)")
        
        return cleanup_result

def main():
    """Command line interface for log management"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Manage gameplay logs")
    parser.add_argument("--status", action="store_true", help="Show log status")
    parser.add_argument("--cleanup", action="store_true", help="Clean up old logs")
    parser.add_argument("--stats", action="store_true", help="Show detailed log statistics")
    parser.add_argument("--max-logs", type=int, default=10, help="Maximum logs to keep (default: 10)")
    parser.add_argument("--logs-dir", default="logs", help="Logs directory (default: logs)")
    parser.add_argument("--no-archive", action="store_true", help="Delete old logs instead of archiving")
    parser.add_argument("--extract", metavar="ARCHIVE_FILE", help="Extract an archived log file")
    
    args = parser.parse_args()
    
    log_manager = LogManager(args.logs_dir, args.max_logs, archive_logs=not args.no_archive)
    
    if args.status:
        status = log_manager.get_log_status()
        print(f"\n📊 LOG STATUS")
        print(f"{'='*50}")
        print(f"Active logs: {status['total_logs']}")
        print(f"Archived logs: {status['archived_logs']}")
        print(f"Max active logs: {args.max_logs}")
        
        if status['newest_log']:
            print(f"\nNewest log: {status['newest_log']['name']}")
            print(f"Created: {status['newest_log']['created']}")
            
            print(f"\nOldest log: {status['oldest_log']['name']}")
            print(f"Created: {status['oldest_log']['created']}")
        
        if status['needs_cleanup']:
            print(f"\n⚠️  Cleanup needed: {status['logs_to_remove']} logs to process")
            if not args.no_archive:
                print(f"   These logs will be compressed and archived")
            else:
                print(f"   These logs will be permanently deleted")
        else:
            print("\n✅ No cleanup needed")
    
    if args.stats:
        stats = log_manager.get_log_statistics()
        print(f"\n📈 LOG STATISTICS")
        print(f"{'='*50}")
        
        # Active logs stats
        print(f"ACTIVE LOGS:")
        print(f"  Count: {stats['active_logs']['count']} logs")
        print(f"  Total size: {stats['active_logs']['total_size'] / 1024:.1f} KB")
        if stats['active_logs']['count'] > 0:
            print(f"  Average size: {stats['active_logs']['avg_size'] / 1024:.1f} KB per log")
        
        # Date range for active logs
        if stats['date_range']['active']['oldest']:
            print(f"  Date range: {stats['date_range']['active']['oldest']} to {stats['date_range']['active']['newest']}")
        
        # Archive stats
        print(f"\nARCHIVED LOGS:")
        print(f"  Count: {stats['archived_logs']['count']} logs")
        print(f"  Total size: {stats['archived_logs']['total_size'] / 1024:.1f} KB")
        if stats['archived_logs']['count'] > 0:
            print(f"  Average size: {stats['archived_logs']['avg_size'] / 1024:.1f} KB per archive")
            print(f"  Average compression: {stats['archived_logs']['avg_compression_ratio']:.1f}% reduction")
            print(f"  Storage saved: {stats['storage_saved'] / 1024:.1f} KB")
        
        # Date range for archived logs
        if stats['date_range']['archive']['oldest']:
            print(f"  Date range: {stats['date_range']['archive']['oldest']} to {stats['date_range']['archive']['newest']}")
        
        # Total stats
        total_logs = stats['active_logs']['count'] + stats['archived_logs']['count']
        total_size = (stats['active_logs']['total_size'] + stats['archived_logs']['total_size']) / 1024
        print(f"\nTOTAL:")
        print(f"  Logs managed: {total_logs}")
        print(f"  Total storage: {total_size:.1f} KB")
    
    if args.extract:
        try:
            archive_path = Path(args.logs_dir) / "archive" / args.extract
            if not archive_path.exists() and not args.extract.endswith('.gz'):
                archive_path = Path(args.logs_dir) / "archive" / f"{args.extract}.gz"
            
            if not archive_path.exists():
                print(f"❌ Archive not found: {args.extract}")
                return
            
            # Extract to original filename in logs directory
            output_path = Path(args.logs_dir) / archive_path.stem
            
            with gzip.open(archive_path, 'rb') as f_in:
                with open(output_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            
            print(f"✅ Extracted {archive_path.name} to {output_path.name}")
            print(f"   Original size: {output_path.stat().st_size / 1024:.1f} KB")
            print(f"   Compressed size: {archive_path.stat().st_size / 1024:.1f} KB")
            print(f"   Compression ratio: {(1 - (archive_path.stat().st_size / output_path.stat().st_size)) * 100:.1f}%")
        except Exception as e:
            print(f"❌ Failed to extract archive: {e}")
    
    if args.cleanup:
        print(f"\n🧹 CLEANING UP LOGS")
        print(f"{'='*50}")
        result = log_manager.cleanup_old_logs()
        
        if result['cleaned']:
            if args.no_archive:
                print(f"✅ Removed {result['removed_count']} old logs")
                print(f"📊 Kept {result['kept_logs']} most recent logs")
                for filename in result['removed_files']:
                    print(f"   🗑️  {filename}")
            else:
                print(f"✅ Archived {result['archived_count']} old logs")
                print(f"📊 Kept {result['kept_logs']} most recent logs")
                
                # Show compression stats if available
                if result.get('compression_stats'):
                    total_original = sum(stat['original_size'] for stat in result['compression_stats'])
                    total_compressed = sum(stat['compressed_size'] for stat in result['compression_stats'])
                    avg_ratio = (1 - (total_compressed / total_original)) * 100 if total_original > 0 else 0
                    
                    print(f"\n📦 COMPRESSION RESULTS:")
                    print(f"   Original size: {total_original / 1024:.1f} KB")
                    print(f"   Compressed size: {total_compressed / 1024:.1f} KB")
                    print(f"   Space saved: {(total_original - total_compressed) / 1024:.1f} KB ({avg_ratio:.1f}%)")
        else:
            print(f"✅ No cleanup needed ({result['total_logs']} logs, max {args.max_logs})")

if __name__ == "__main__":
    main()