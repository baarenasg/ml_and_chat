if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    import uvicorn

    load_dotenv(dotenv_path="src/applications/config/.env.local")
    uvicorn.run(
        "src.applications.app_service:app", host="0.0.0.0", port=8000, reload=True, log_level="debug"
    )
