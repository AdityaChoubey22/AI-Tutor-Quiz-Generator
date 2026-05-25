# formatting the response provided by the AI model
def format_tutoring_response(content, learning_style):
    """Helper function to format the response from the AI model based on the learning style."""

    if learning_style == "Visual":
        return content + "\n\n*Note: Visualize these concepts as you read for better understanding.*"
    elif learning_style == "Hands-on":
        return content + "\n\n*Note: Try working through the examples yourself to reinforce your learning.*"
    else:
        return content
