# Setting up Google sign-in and saving

Qubi uses two free services:

- **Google sign-in** (Streamlit's `st.login`) knows who you are.
- **Supabase** saves your progress in a table.

It takes about 30 minutes. Until it's done, Qubi still runs, but only "Try it as a guest" works and nothing is saved.

Never put your keys on GitHub. They go in `.streamlit/secrets.toml`, which `.gitignore` already keeps off GitHub, and in Streamlit Cloud's Secrets box.

---

## 1. Supabase (the database)

1. Go to **supabase.com** and sign up (signing up with GitHub is easiest).
2. Click **New project**. Name it `qubi`, make up a database password (save it somewhere), pick the region **East US**, and click **Create**. Wait about 2 minutes.
3. In the left bar click **SQL Editor**, then **New query**. Paste this and click **Run**:

   ```sql
   create table progress (
     email text primary key,
     data jsonb not null,
     updated_at timestamptz not null default now()
   );
   alter table progress enable row level security;
   ```

   The last line locks the table so only Qubi's secret key can read it.
4. Copy two things into a note:
   - **Project URL.** Click **Connect** at the top (or **Project Settings → Data API**). It looks like `https://abcdefgh.supabase.co`.
   - **Secret key.** Go to **Project Settings → API Keys** and find the **Secret keys** section. Copy the key that starts with `sb_secret_`. If you only see legacy keys, use the **service_role** key. **Don't** use the publishable or anon key.

## 2. Google sign-in

1. Go to **console.cloud.google.com** and sign in. At the top, click the project picker, then **New project**. Name it `Qubi` and click **Create**, then make sure it's selected.
2. In the search bar type **Google Auth Platform** and open it. Click **Get started**.
   - App name: `Qubi`. User support email: your email.
   - Audience: **External**.
   - Contact email: your email. Agree, then **Create**.
3. Click **Audience** on the left, then **Publish app**, and confirm. Without this, only people you add by hand can sign in, and the judges couldn't. Qubi only asks for name and email, so Google doesn't need to review it.
4. Click **Clients** on the left, then **Create client**.
   - Application type: **Web application**. Name: `Qubi`.
   - Under **Authorized redirect URIs**, add both of these (use your real app address for the second):
     - `http://localhost:8501/oauth2callback`
     - `https://YOUR-APP.streamlit.app/oauth2callback`
   - Click **Create**, then copy the **Client ID** and **Client secret**.

## 3. Your secrets file (for running on your Mac)

1. Make a random cookie secret. In the VS Code terminal run:

   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

2. Create the file `.streamlit/secrets.toml` (in the same folder as `config.toml`) and paste this in, filling in your values:

   ```toml
   [auth]
   redirect_uri = "http://localhost:8501/oauth2callback"
   cookie_secret = "PASTE THE RANDOM STRING"

   [auth.google]
   client_id = "PASTE CLIENT ID"
   client_secret = "PASTE CLIENT SECRET"
   server_metadata_url = "https://accounts.google.com/.well-known/openid-configuration"

   [supabase]
   url = "https://abcdefgh.supabase.co"
   key = "sb_secret_PASTE"
   ```

3. Install the new packages and start Qubi:

   ```bash
   pip install -r requirements.txt
   streamlit run main.py
   ```

   It has to run on port 8501 (the normal one) to match the redirect address.
4. Click **Get started**, then **Continue with Google**. After you pick your daily goal, open Supabase and go to **Table Editor → progress**. You should see a row with your email.

## 4. Streamlit Cloud (the live site)

1. Push the code to GitHub. `secrets.toml` won't go with it, and that's what we want.
2. In Streamlit Cloud open your app, then **⋮ → Settings → Secrets**. Paste the same text as your `secrets.toml`, with one change:

   ```toml
   redirect_uri = "https://YOUR-APP.streamlit.app/oauth2callback"
   ```

3. Click **Save**. The app restarts by itself. Try signing in on the live site.

## If something goes wrong

| What you see | What to check |
|---|---|
| Google says `redirect_uri_mismatch` | The redirect URI in Google must match `redirect_uri` exactly, including `http` vs `https` and no `/` at the end. |
| "Access blocked" or "app not verified" | Step 2.3: the app must be published, not "Testing". |
| The Google button is grey | `secrets.toml` is missing, misnamed, or not in the `.streamlit` folder. |
| The sidebar says "Saving is off right now" | Check the Supabase URL and key, and that step 1.3's table exists. |