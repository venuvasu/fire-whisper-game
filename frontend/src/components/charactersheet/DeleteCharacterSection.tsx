import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../../auth/AuthContext";
import { apiRequest } from "../../utils/apiClient";

const DeleteCharacterSection = ({ character, characterId }) => {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);
  const [deleteConfirmText, setDeleteConfirmText] = useState("");

  const handleDeleteCharacter = async () => {
    setIsDeleting(true);
    try {
      await apiRequest({
        path: `/deletecharacter?character_id=${characterId}`,
        method: "DELETE",
        token: user.id_token,
      });

      navigate("/");
    } catch (err) {
      console.error("Failed to delete character:", err);
      // Handle error - maybe show an error message
      setIsDeleting(false);
      setShowDeleteConfirm(false);
      setDeleteConfirmText("");
    }
  };

  const handleCancelDelete = () => {
    setShowDeleteConfirm(false);
    setDeleteConfirmText("");
  };

  const isDeleteConfirmValid = deleteConfirmText === character?.IDENTITY.name;

  return (
    <div className="border-t border-[#3E2713] pt-8 mt-12">
      <div className="bg-red-50 border border-red-200 rounded-xl p-6">
        <h3 className="text-xl font-bold text-red-700 mb-3">Danger Zone</h3>
        <p className="text-red-600 mb-4">
          Permanently delete this character. This action cannot be undone.
        </p>

        {!showDeleteConfirm ? (
          <button
            onClick={() => setShowDeleteConfirm(true)}
            className="bg-red-600 hover:bg-red-700 text-white font-bold py-3 px-6 rounded-lg transition-colors duration-200 border border-red-700"
          >
            Delete Character
          </button>
        ) : (
          <div className="space-y-4">
            <p className="text-red-800 font-semibold">
              Are you sure you want to delete "{character.IDENTITY.name}"?
            </p>
            <p className="text-red-700 text-sm">
              Type the character's name below to confirm deletion:
            </p>
            <div className="space-y-3">
              <input
                type="text"
                value={deleteConfirmText}
                onChange={(e) => setDeleteConfirmText(e.target.value)}
                placeholder={character.IDENTITY.name}
                className="w-full px-4 py-2 border-2 border-red-300 rounded-lg focus:border-red-500 focus:outline-none bg-white text-gray-900"
                disabled={isDeleting}
              />
              <div className="flex gap-3">
                <button
                  onClick={handleDeleteCharacter}
                  disabled={isDeleting || !isDeleteConfirmValid}
                  className={`font-bold py-3 px-6 rounded-lg transition-colors duration-200 border ${
                    isDeleteConfirmValid && !isDeleting
                      ? "bg-red-600 hover:bg-red-700 text-white border-red-700"
                      : "bg-gray-300 text-gray-500 border-gray-400 cursor-not-allowed"
                  }`}
                >
                  {isDeleting ? "Deleting..." : "Yes, Delete Forever"}
                </button>
                <button
                  onClick={handleCancelDelete}
                  disabled={isDeleting}
                  className="bg-gray-300 hover:bg-gray-400 disabled:bg-gray-200 text-gray-700 font-bold py-3 px-6 rounded-lg transition-colors duration-200 border border-gray-400"
                >
                  Cancel
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default DeleteCharacterSection;
