from dotenv import load_dotenv
from replicate.client import Client
from transformers import AutoTokenizer  # Add this import

import gradio as gr
import json
import time
import re
import os

# CSS styling
css = """
.category-legend{display:none}
button{height: 60px}
"""

# Constants
MASK_TOKEN = "[MASK]"

# Initialize environment and client
load_dotenv()
replicate = Client(api_token=os.environ.get("REPLICATE_API_TOKEN"))

# Load tokenizer for formatting chat template properly
tokenizer = AutoTokenizer.from_pretrained(
    "GSAI-ML/LLaDA-8B-Instruct", trust_remote_code=True
)


def parse_constraints(constraints_text):
    """Parse constraints in format: 'position:word, position:word, ...'"""
    constraints = {}
    if not constraints_text:
        return constraints

    parts = constraints_text.split(",")
    for part in parts:
        if ":" not in part:
            continue
        pos_str, word = part.split(":", 1)
        try:
            pos = int(pos_str.strip())
            word = word.strip()
            if word and pos >= 0:
                constraints[pos] = word
        except ValueError:
            continue

    return constraints


def format_chat_history(history):
    """Format chat history for the LLaDA model"""
    messages = []
    for user_msg, assistant_msg in history:
        messages.append({"role": "user", "content": user_msg})
        if assistant_msg:  # Skip if None (for the latest user message)
            messages.append({"role": "assistant", "content": assistant_msg})

    return messages


def generate_response_with_visualization(
    messages,
    gen_length=64,
    steps=32,
    constraints=None,
    temperature=0.5,
    cfg_scale=0.0,
    block_length=32,
    remasking="low_confidence",
):
    """Generate text using the Replicate API version of LLaDA with visualization"""

    # Process constraints
    if constraints is None:
        constraints = {}
    constraints_json = json.dumps(constraints)

    # Format chat using the tokenizer's chat template
    chat_input = tokenizer.apply_chat_template(
        messages, add_generation_prompt=True, tokenize=False
    )

    # Call Replicate API
    output = replicate.run(
        "spuuntries/llada-8b-kcv:e8b3ac0457f822454d662dec90edcac05f6e5947a50b55f92b22aa996acbf780",
        input={
            "steps": steps,
            "prompt": chat_input,
            "cfg_scale": cfg_scale,
            "remasking": remasking,
            "max_tokens": gen_length,
            "constraints": constraints_json,
            "temperature": temperature,
            "block_length": block_length,
            "prompt_template": "{prompt}",  # Use the already formatted prompt
        },
        wait=False,
    )

    # Extract final response and states
    final_output = output["final_output"]
    states = output["states"]

    # Extract only the last assistant response by finding the last occurrence
    # of the assistant header pattern
    last_assistant_pattern = r"<\|start_header_id\|>assistant<\|end_header_id\|>\n"
    last_assistant_match = list(re.finditer(last_assistant_pattern, final_output))

    if last_assistant_match:
        # Get the last match
        last_match = last_assistant_match[-1]
        # Start position of the actual content (after the header)
        start_pos = last_match.end()
        # Extract everything from this position to the end or until end token
        end_pattern = r"<\|endoftext\|>|<\|start_header_id\|>"
        end_match = re.search(end_pattern, final_output[start_pos:])

        if end_match:
            end_pos = start_pos + end_match.start()
            response_text = final_output[start_pos:end_pos].strip()
        else:
            response_text = final_output[start_pos:].strip()
    else:
        response_text = "Error: Could not parse the model response."

    # Process states for visualization
    visualization_states = []

    # Add initial state (all masked)
    initial_state = [(MASK_TOKEN, "#444444") for _ in range(gen_length)]
    visualization_states.append(initial_state)

    for state in states:
        # Similar parsing for visualization states
        last_assistant_match = list(re.finditer(last_assistant_pattern, state))

        if last_assistant_match:
            last_match = last_assistant_match[-1]
            start_pos = last_match.end()
            tokens_text = state[start_pos:].strip()
            tokens = tokens_text.split()

            current_state = []
            for token in tokens:
                if token == "[MASK]":
                    current_state.append((token, "#444444"))  # Dark gray for masks
                else:
                    current_state.append(
                        (token, "#6699CC")
                    )  # Light blue for revealed tokens

            visualization_states.append(current_state)
        else:
            # Fallback if we can't parse properly
            visualization_states.append(
                [(MASK_TOKEN, "#FF6666")]
            )  # Red mask as error indicator

    return visualization_states, response_text.replace("<|eot_id|>", "")


def create_chatbot_demo():
    with gr.Blocks(css=css) as demo:
        gr.Markdown("# LLaDA - Large Language Diffusion Model Demo")
        gr.Markdown(
            "[model](https://huggingface.co/GSAI-ML/LLaDA-8B-Instruct), [project page](https://ml-gsai.github.io/LLaDA-demo/)"
        )

        # STATE MANAGEMENT
        chat_history = gr.State([])

        # Current response text box (hidden)
        current_response = gr.Textbox(
            label="Current Response",
            placeholder="The assistant's response will appear here...",
            lines=3,
            visible=False,
        )

        # UI COMPONENTS
        with gr.Row():
            with gr.Column(scale=3):
                chatbot_ui = gr.Chatbot(label="Conversation", height=500)

                # Message input
                with gr.Group():
                    with gr.Row():
                        user_input = gr.Textbox(
                            label="Your Message",
                            placeholder="Type your message here...",
                            show_label=False,
                        )
                        send_btn = gr.Button("Send")

                constraints_input = gr.Textbox(
                    label="Word Constraints",
                    info="Format: 'position:word, position:word, ...' Example: '0:Once, 5:upon, 10:time'",
                    placeholder="0:Once, 5:upon, 10:time",
                    value="",
                )
            with gr.Column(scale=2):
                output_vis = gr.HighlightedText(
                    label="Denoising Process Visualization",
                    combine_adjacent=False,
                    show_legend=True,
                )

        # Advanced generation settings
        with gr.Accordion("Generation Settings", open=False):
            with gr.Row():
                gen_length = gr.Slider(
                    minimum=16, maximum=128, value=64, step=8, label="Generation Length"
                )
                steps = gr.Slider(
                    minimum=8, maximum=128, value=32, step=4, label="Denoising Steps"
                )
            with gr.Row():
                temperature = gr.Slider(
                    minimum=0.0, maximum=1.0, value=0.5, step=0.1, label="Temperature"
                )
                cfg_scale = gr.Slider(
                    minimum=0.0, maximum=2.0, value=0.0, step=0.1, label="CFG Scale"
                )
            with gr.Row():
                block_length = gr.Slider(
                    minimum=8, maximum=128, value=32, step=8, label="Block Length"
                )
                remasking_strategy = gr.Radio(
                    choices=["low_confidence", "random"],
                    value="low_confidence",
                    label="Remasking Strategy",
                )
            with gr.Row():
                visualization_delay = gr.Slider(
                    minimum=0.0,
                    maximum=1.0,
                    value=0.05,
                    step=0.01,
                    label="Visualization Delay (seconds)",
                )

        # Clear button
        clear_btn = gr.Button("Clear Conversation")

        def add_message(history, message, response):
            """Add a message pair to the history and return the updated history"""
            history = history.copy()
            history.append([message, response])
            return history

        def user_message_submitted(
            message, history, gen_length, steps, constraints, delay
        ):
            """Process a submitted user message"""
            # Skip empty messages
            if not message.strip():
                # Return current state unchanged
                history_for_display = history.copy()
                return history, history_for_display, "", [], ""

            # Add user message to history
            history = add_message(history, message, None)

            # Format for display - temporarily show user message with empty response
            history_for_display = history.copy()

            # Clear the input
            message_out = ""

            # Return immediately to update UI with user message
            return history, history_for_display, message_out, [], ""

        def bot_response(
            history,
            gen_length,
            steps,
            constraints,
            delay,
            temperature,
            cfg_scale,
            block_length,
            remasking,
        ):
            """Generate bot response for the latest message"""
            if not history:
                return history, [], ""

            try:
                # Format all messages except the last one (which has no response yet)
                messages = format_chat_history(history[:-1])

                # Add the last user message
                messages.append({"role": "user", "content": history[-1][0]})

                # Parse constraints
                parsed_constraints = parse_constraints(constraints)

                # Generate response with visualization
                vis_states, response_text = generate_response_with_visualization(
                    messages,
                    gen_length=gen_length,
                    steps=steps,
                    constraints=parsed_constraints,
                    temperature=temperature,
                    cfg_scale=cfg_scale,
                    block_length=block_length,
                    remasking=remasking,
                )

                # Update history with the assistant's response
                history[-1][1] = response_text

                # Return the initial state immediately
                yield history, vis_states[0], response_text

                # Then animate through visualization states
                for state in vis_states[1:]:
                    time.sleep(delay)
                    yield history, state, response_text

            except Exception as e:
                error_msg = f"Error: {str(e)}"
                print(error_msg)

                # Show error in visualization
                error_vis = [(error_msg, "red")]

                # Don't update history with error
                yield history, error_vis, error_msg

        def clear_conversation():
            """Clear the conversation history"""
            return [], [], "", []

        # EVENT HANDLERS

        # Clear button handler
        clear_btn.click(
            fn=clear_conversation,
            inputs=[],
            outputs=[chat_history, chatbot_ui, current_response, output_vis],
        )

        # User message submission flow (2-step process)
        # Step 1: Add user message to history and update UI
        msg_submit = user_input.submit(
            fn=user_message_submitted,
            inputs=[
                user_input,
                chat_history,
                gen_length,
                steps,
                constraints_input,
                visualization_delay,
            ],
            outputs=[
                chat_history,
                chatbot_ui,
                user_input,
                output_vis,
                current_response,
            ],
        )

        # Also connect the send button
        send_click = send_btn.click(
            fn=user_message_submitted,
            inputs=[
                user_input,
                chat_history,
                gen_length,
                steps,
                constraints_input,
                visualization_delay,
            ],
            outputs=[
                chat_history,
                chatbot_ui,
                user_input,
                output_vis,
                current_response,
            ],
        )

        # Step 2: Generate bot response
        # This happens after the user message is displayed
        msg_submit.then(
            fn=bot_response,
            inputs=[
                chat_history,
                gen_length,
                steps,
                constraints_input,
                visualization_delay,
                temperature,
                cfg_scale,
                block_length,
                remasking_strategy,
            ],
            outputs=[chatbot_ui, output_vis, current_response],
        )

        send_click.then(
            fn=bot_response,
            inputs=[
                chat_history,
                gen_length,
                steps,
                constraints_input,
                visualization_delay,
                temperature,
                cfg_scale,
                block_length,
                remasking_strategy,
            ],
            outputs=[chatbot_ui, output_vis, current_response],
        )

    return demo


# Launch the demo
if __name__ == "__main__":
    demo = create_chatbot_demo()
    demo.queue().launch(server_name="0.0.0.0")
