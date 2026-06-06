# ⚡ Nexus Lightning Backend: Ready-to-Use Core in One File

Stop wasting hours setting up databases, user authentication, and API routing for your new web apps or indie games. **Nexus Lightning Backend** gives you a fully functional, secure, and production-ready server environment in a single Python file.

## 🚀 Why Use This?

Every time a developer starts a project, they lose the first day coding the same boring boilerplate: User Login, Registration, Token verification, and Database connections. 

This engine solves that instantly. Run it, and you get a local **Firebase/Supabase alternative** powered by a high-performance Python engine.

## ✨ Implemented Modules

* **Instant SQLite NoSQL-like Database:** Key-Value database storage out of the box with zero external database installs.
* **Token-Based Authentication:** Clean Register and Login endpoints generating secure access hashes (`auth tokens`).
* **Protected Cloud-Data Layer:** Secure data storage endpoints (`/data/save` and `/data/get`) restricted via token verification.
* **Automated Swagger Documentation:** Visually test and manage your entire backend by opening `/docs` in your browser.

## 🛠️ Launch at Lightning Speed

1. Install the high-speed requirements:
   ```bash
   pip install fastapi uvicorn pydantic
```
2. Run the engine:
```bash
uvicorn server:app --reload
```
3.
```bash
Open http://127.0.0.1:8000/docs in your browser. You will see a beautiful, fully interactive GUI to test your database and users instantly.
```
### 📄 License
​MIT License. Download, run, and start building your app at lightspeed!