from chains.coding_chain import coding_chain

def show_menu():
    print("Choose an option:")
    print("=" * 70)
    print("1. Ask a coding question")
    print("2. Generate Code Snippet")
    print("3. Explain Code")
    print("4. Exit")


def get_user_query(choice):
    if choice == "1":
        return input("Ask coding question: ")
    elif choice == "2":
        return input("Provide a description for code snippet generation: ")
    elif choice == "3":
        return input("Paste the code you want to be explained: ")
    else:
        return None

def main():

    while True:
        show_menu()
        choice = input("Enter your choice (1-4): ")

        if choice == "4":
            print("Thankyou for using AI Coding Assistant")
            break

        if choice not in ["1", "2", "3"]:
            print("Invalid choice. Please try again.")
            continue

        question = get_user_query(choice)
        if not question:
            continue

        print("\nGenerating Response")
        task_map = {
            "1": "Answer the coding question",
            "2": "Generate production-ready source code",
            "3": "Explain the provided source code"
        }

        # response = coding_chain.invoke(
        #     {
        #         "task": task_map[choice],
        #         "question": question
        #     }
        # )

        for response in coding_chain.stream(
            {
                "task": task_map[choice],
                "question": question
            }
        ):
            print(response, end="", flush=True)
        
        print("\n" + "=" * 70)


if __name__ == "__main__":
    main()