from solution.user_interface.cli import run_cli


def main() -> None:
    try:
        run_cli()
    except Exception:
        print("Something went wrong. Please try again later.")


if __name__ == "__main__":
    main()


# Terminal 1 - Start the API:
# RUN -> fastapi dev solution/api/main.py

# Terminal 2 - Start the UI:
# RUN -> python main.py
