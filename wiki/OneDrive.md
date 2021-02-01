### Notice
To make Nazurin bot has authority to access OneDrive resources, you need to finish two main steps:
1. Registry an app in Azure Active Directory (AAD)
2. Log in an sample app provided by Microsoft to gain REFRESH_TOKEN for Nazurin bot

These mean that you must have an account which owns an Azure Active Directory subscription and prepare an account which owns OneDrive Service(The two can be the same).

For Microsoft organization account(work or school account), you can see your subscription status [here](https://portal.office.com/account/?ref=MeControl#subscriptions).

For simple Microsoft account, you may need to purchase Azure Active Directory subscription.

### Instructions

#### Register the app

1. Go to Azure Active Directory for [App registrations](https://go.microsoft.com/fwlink/?linkid=2083908)
2. Select **New registration**.
3. Enter the app's registration information:
   - In the **Name** section, enter the name you like.
   - Change **Supported account types** to **Accounts in any organizational directory and personal Microsoft accounts**.
   - In the Redirect URI (optional) section, enter the following redirect URIs: `http://localhost:5000/getAToken`.
4. Select **Register** to create the application.
5. On the app **Overview** page, find the **Application (client) ID** value and record it for later replacing.
6. On the **Certificates & secrets** page, in the **Client secrets** section, choose **New client secret**:

   - Type a key description or just leave it blank.
   - Select a key duration of either **In 1 year**, **In 2 years**, or **Never Expires**.
   - When you press the **Add** button, the key value will be displayed, copy, and record it for replacing.

7. On the **API permissions** page
   - Click the **Add a permission** button and then,
   - Select **Microsoft APIs** tab,
   - In the *Commonly used Microsoft APIs* section, click on **Microsoft Graph**
   - In the **Delegated permissions** section, check the pessimision: **Files.Read**, **Files.ReadWrite**. Use the search box if necessary.
   - Select the **Add permissions** button

#### Log in an sample app

To start this step, your environment needs `git`, `python 3.x` and a brower.

1. Clone the sample app

    ```shell
    git clone https://github.com/Azure-Samples/ms-identity-python-webapp.git
    ```

2. Use an editor to modify the config file

    + Open `app_config.py`
    + Paste the **Application (client) ID** into the value holder of **CLIENT_ID**
    + Paste the secret into the value holder of **CLIENT_SECRET**
    + Enter the value of **SCOPE**,after which it look like this:
        ```python
        SCOPE = ["User.ReadBasic.All","Files.Read","Files.ReadWrite"]
        ```
    + ONLY when the `REDIRECT_PATH` is different from the part of the url you enter in the Redirect URI section should you modify it.
    + Save the changes

3. Use an editor to modify the code of the sample app to gain the `REFRESH_TOKEN`

    + Open `app.py`
    + In the function `authorized()`, make a new line after `_save_cache(cache)`
    + Paste `print(session["token_cache"])`, and pay attention to the indentation for you are modifying Python code
    + Save the change
4. Run the code

    ```shell
    pip install -r requirements.txt
    ```

    ```shell
    flask run --host localhost --port 5000
    ```

    The port value needs to match what you've set up. After running this, a brower window will pop up and you can login the account you prepare for storing the pictures.

5. After login, you can find the refresh_token in the terminal. It's the value of "RefreshToken" -> "secret"

### Configuration
#### `STORAGE`
Append `'OneDrive'`
#### `OD_CLIENT`
The **Application (client) ID** you gained from AAD
#### `OD_SECRET`
The secret you have set up in AAD
#### `OD_RF_TOKEN`
The token you gained from the terminal

Notice that this refresh token is only for the first-time auth of Nazurin bot, after which Nazurin can gain tokens by itself