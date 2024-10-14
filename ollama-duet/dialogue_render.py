import json


def render_dialogue_as_html(
    dialogue, output_file="dialogue.html", avatar1="👩‍🔬", avatar2="🧑‍🌾"
):
    """
    Renders a JSON dialogue transcript as an HTML page with styled messages.

    Parameters:
    - dialogue (list): List of dictionaries with 'role' and 'content' keys.
    - output_file (str): Filename for the output HTML. Defaults to 'dialogue.html'.
    """

    # Define the mapping of roles to alignment and avatar emojis
    role_mapping = {
        "Plant Expert": {
            "align": "left",
            "avatar": avatar1,  # Scientist emoji for expert
        },
        "Plant Novice": {
            "align": "right",
            "avatar": avatar2,
        },  # Farmer emoji for novice
    }

    # Start building the HTML content
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <title>Dialogue Transcript</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 20px;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
            }
            .message {
                display: flex;
                margin-bottom: 20px;
                align-items: flex-start;
            }
            .message.left {
                flex-direction: row;
            }
            .message.right {
                flex-direction: row-reverse;
            }
            .avatar {
                font-size: 50px;
                margin: 0 10px;
                line-height: 1;
            }
            .bubble {
                max-width: 70%;
                padding: 10px 15px;
                border-radius: 15px;
                position: relative;
                background-color: #ffffff;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                word-wrap: break-word;
                font-size: 16px;
                line-height: 1.4;
            }
            .left .bubble {
                background-color: #007BFF;
                color: #ffffff;
                border-bottom-left-radius: 0;
            }
            .right .bubble {
                background-color: #28A745;
                color: #ffffff;
                border-bottom-right-radius: 0;
            }
            @media (max-width: 600px) {
                .bubble {
                    max-width: 85%;
                }
                .avatar {
                    font-size: 30px;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
    """

    # Iterate over each message in the dialogue
    for i, entry in enumerate(dialogue):
        role = entry.get("role", "Unknown")
        content = entry.get("content", "")

        if i % 2 == 0:
            avatar = avatar1
            alignment = "left"
        else:
            alignment = "right"
            avatar = avatar2

        # Escape HTML special characters in content
        content = (
            content.replace("&", "&amp;")
            .replace("<", "<")
            .replace(">", ">")
            .replace("\n", "<br>")
        )

        message_html = f"""
            <div class="message {alignment}">
                <div class="avatar">{avatar}</div>
                <div class="bubble">
                    <strong>{role}</strong><br>
                    {content}
                </div>
            </div>
        """
        html_content += message_html

    # Close the container and body tags
    html_content += """
        </div>
    </body>
    </html>
    """

    # Write the HTML content to the output file
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(html_content)

    print(f"Dialogue has been rendered to {output_file}")
