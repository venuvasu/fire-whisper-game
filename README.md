## Fire Whisper API Backend

This repository contains the Python-based AWS Lambda backend for the Fire Whisper API.

## Setting Up a New Environment

To set up a new environment or deploy to a new AWS account, you’ll need to provision several AWS resources. This section walks you through that process.

**Prerequisites:**  
Make sure the following tools are installed before proceeding:

- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html)
- [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)

You will also need to configure IAM privileges for each, which are documented on their pages.

### Choosing an Environment

Before starting the setup, decide which environment you want to deploy to.  
**Allowed values** (case-sensitive):

- `Dev`
- `Beta`

For local development, it's recommended to use `Dev`.  
However, any value is fine—as long as you use the same one consistently within the same AWS account.

### Set Up Cognito User Pool

A Cognito User Pool is required for user authentication. Follow these steps to create and configure it.

---

#### 🛠️ Create a User Pool

1. In the AWS Console, go to **Amazon Cognito** → **User Pools** and click **"Create user pool"**.
2. **Name the User Pool** – You can choose any name, but we recommend:  
   `Fire-Whisper-{Environment}` (e.g., `Fire-Whisper-Dev`)
3. Under **Sign-in options**, select `Username` and `Email` (recommended).
4. Under **Required attributes**, at a minimum select `Email`.

---

#### 🔧 Configure App Client

Once your User Pool is created:

1. Go to the **"App clients"** tab.
2. Select your **App client**, then go to the **"Login pages"** section under **App client information**.
3. In **Managed login pages configuration**, update the following fields via the edit:

##### ✅ Allowed Callback URLs

- You must include both the base domain **and** the `/callback` path for each allowed frontend domain.
- Example for local development with the `fire-whisper-ui`:
  - `http://localhost:5173/` **(trailing slash required)**
  - `http://localhost:5173/callback`
- Multiple domains can be added to the same User Pool.

##### ✅ Allowed Sign-Out URLs

- List each base domain where users should be redirected after signing out.
- Example:
  - `http://localhost:5173/` **(trailing slash required)**

##### ✅ OpenID Connect Scopes

- Ensure the following scopes are enabled:
  - `email`
  - `openid`
  - `phone`
  - `profile` (must be manually added)

> ⚠️ **Note:** If any of these settings are incorrect, authentication via the frontend may fail to complete the redirect flow.

### Set Up DynamoDB Tables

You will need to create **three DynamoDB tables** using the AWS Console.  
Each table should use the **default settings** and include the environment name as a suffix.

#### Table Naming Convention

Use the following format for table names:

- `FW_Characters_{Environment}`
- `FW_Sagas_{Environment}`
- `FW_UserData_{Environment}`

For example, if you're deploying to the `Dev` environment, your table names should be:

- `FW_Characters_Dev`
- `FW_Sagas_Dev`
- `FW_UserData_Dev`

> 💡 Make sure the environment suffix (e.g. `Dev`, `Beta`) matches the value used in your `.env` file and other configuration steps.

### Create a Deployer S3 Bucket

An S3 bucket is required to store and serve your deployment packages during the build and deploy process. This bucket will be used by AWS SAM to stage artifacts before deploying your Lambda functions.

#### Steps to Create the Bucket

1. **Go to the AWS Console** and navigate to **S3**.
2. Click **"Create bucket"**.
3. Choose a **globally unique name** for your bucket (e.g., `fire-whisper-deployer`).
4. Select the **region** where your Lambda functions will be deployed. (this should be where you intend to deploy)
5. Click **"Create bucket"**.

### Setup .env file for Lambda's

Create a .env file in the root of the fire-whisper-lambda-api. This file will indicate the specific environment and Cognito settings to deploy to. It must be consistent with the above setup steps.

```
FIREWHISPER_ENV=Dev
FIREWHISPER_USER_POOL=XXX
FIREWHISPER_USER_POOL_CLIENT=XXX
```

#### `.env` Variable Reference

| Key                            | Description                                                              | Example Values       |
| ------------------------------ | ------------------------------------------------------------------------ | -------------------- |
| `FIREWHISPER_ENV`              | The name of the environment to deploy to. Used for naming suffixes.      | `Dev`, `Beta`        |
| `FIREWHISPER_USER_POOL`        | Cognito User Pool ID (visible in the AWS Cognito console).               | e.g. `us-east-1_ABC` |
| `FIREWHISPER_USER_POOL_CLIENT` | Cognito User Pool App Client ID (visible under the app client settings). | e.g. `123abc456xyz`  |

### Package and Deploy

To build and prepare your Lambda functions for deployment, run:

```bash
make package
```

This will compile the code and upload the deployment artifacts to your designated S3 bucket.

Then, deploy the packaged application using:

```bash
make deploy
```

Once deployment is complete, you can view and manage your Lambda functions in the [AWS Lambda Console](https://console.aws.amazon.com/lambda/).

### AWS Bedrock Model Permissions

To use Amazon Bedrock in your AWS account, you must request access to individual models.  
If these permissions are not granted, your Lambda functions may fail with authorization errors.

You can manage model access in the **AWS Console** under **Amazon Bedrock** → **Model access** (found in the **Bedrock configuration** section).

#### Required Models for Fire Whisper

The primary models used by Fire Whisper are:

- **Claude 3.5 Haiku**
- **Claude 3 Haiku**

Fire Whisper also supports other models, which may require additional approval depending on your use case. Note you may need to redploy your lambda's after getting approval.
