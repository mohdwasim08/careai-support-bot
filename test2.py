from careai import get_response, update_history

# Start with empty history
chat_history = []

# Turn 1
user1 = "Hi, where is my order?"
reply1 = get_response(chat_history, user1)
print("CareAI:", reply1)
chat_history = update_history(chat_history, user1, reply1)

# Turn 2 — test memory
user2 = "My order number is #4521"
reply2 = get_response(chat_history, user2)
print("\nCareAI:", reply2)
chat_history = update_history(chat_history, user2, reply2)

# Turn 3 — test empathy
user3 = "This is taking too long, I am really frustrated!"
reply3 = get_response(chat_history, user3)
print("\nCareAI:", reply3)