# to communicate gemini llm with the chatbot service
from google import genai
from dotenv import load_dotenv
from databasemodels import Product,chathistory
from typing import List
import os

load_dotenv()


class Chatbotservice:

    def __init__(self, model="gemini-3.5-flash-lite"):
        self.model = model
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.company_name = "U Commerce"
        self.bot_name = "U Commerce Chatbot"

    def get_response(self, prompt):
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt
        )
        return response.text

    def get_chat_history_context(
        self,
        chat_history: List[chathistory],
        limit=10
    ):
        chat_context = ""

        if not chat_history:
            return "This is the start of communication."

        recent_chat_history = (
            chat_history[-limit:]
            if len(chat_history) > limit
            else chat_history
        )

        for chat in recent_chat_history:
            sender_label = "User" if chat.sender == "user" else "Assistant"
            chat_context += f"{sender_label}: {chat.message}\n"

        return chat_context

    def get_products_context(self, products: List[Product]):

        if not products:
            return "No products available."

        categories = {}

        for product in products:

            if product.category not in categories:
                categories[product.category] = []

            categories[product.category].append(product)

        products_context = ""

        for category, category_products in categories.items():

            products_context += f"{category}:\n"

            for product in category_products:

                stock_status = (
                    f"IN STOCK ({product.current_stock})"
                    if product.current_stock > 0
                    else "OUT OF STOCK"
                )

                products_context += (
                    f"- {product.title}: "
                    f"{product.description}: "
                    f"Price is {product.price}: "
                    f"{stock_status}\n"
                )

        return products_context

    def generate_prompt(
        self,
        user_name,
        user_input,
        products_context,
        chat_context
    ):

        prompt = f"""
You are a helpful bot for {self.company_name}.
Your name is {self.bot_name}.

You are here to help users find products and answer their questions.
You are not allowed to ask for user information.

Current user name is {user_name}.

Available products:
{products_context}

Previous conversation:
{chat_context}

Instructions:
- Always address the user by their name ({user_name}).
- Provide accurate product information from the available products list above.
- Check product stock availability before recommending a product.
- If a product is OUT OF STOCK, inform the user politely and suggest an alternative if available.
- Be friendly, professional, and helpful.
- Keep responses short and to the point (2-4 sentences typically).
- If the user asks about products not in the list, politely say you don't have that product.
- Focus on being a sales support assistant: help users find products, check availability, and provide information.

User's question:
{user_input}
"""

        return prompt

    def chat(
        self,
        user_name,
        user_input,
        products: List[Product],
        chat_history: List[chathistory]
    ):

        products_context = self.get_products_context(products)
        chat_context = self.get_chat_history_context(chat_history)

        prompt = self.generate_prompt(
            user_name,
            user_input,
            products_context,
            chat_context
        )

        response = self.get_response(prompt)

        return response


chatbot_service = Chatbotservice()
# from dns.tsig import Key
# from google import Genai
# from dotenv import load_dotenv
# from databasemodels import chathistory,product
# from typing import List
# import os

# load_dotenv()  # Load environment variables from .env file

# class ChatbotService:
#     def __init__(self,model_name="gemini-3.5-flash-lite"):
#         self.model_name = model_name
#         self.client = Genai.Client(api_key=os.getenv("Gemini_API_Key"))
#         self.company_name = "U Commerce"
#         self.bot_name = "U commerce chatBot"

#     def get_response(self, prompt):
#         response = self.client.models.generate_content(
#             model=self.model_name,
#             content=prompt
#         )
#         return response.text

#     def get_chat_history_context(
#             self, 
#             chat_history,
#             limit=10
#     ):
#         chat_context = ""
#         if not chat_history:
#             return "This is the first message in the chat. No previous context available."
#         recent_chat_history = (
#             chat_history[-limit:]
#             if len(chat_history) > limit
#             else chat_history
#         )

#         for chat in recent_chat_history:
#             chat_label = "User" if chat["sender"] == "user" else "Assistant"
#             chat_context += f"{chat_label}: {chat['message']}\n"

#         return chat_context
#     def get_products_context(self, products: List[product]):
#         if not products:
#             return "No products available."
#         categories = {}
#         for product in products:
#             if product.category not in categories:
#                 categories[product.category] = []
#             categories[product.category].append(product)
#         products_context = ""
#         for category, products in categories.items():
#             products_context += f"Category: {category}\n"
#             for product in products:
#                 stock_status = (
#                     f"In Stock ({product.current_stock})" if product.current_stock > 0
#                     else "Out of Stock"
#                 )
#                 products_context += (
#                     f"Product: {product.title}\n"
#                     f" {product.description}\n"
#                     f"Price: ${product.price}\n"
#                     f"Stock Status: {stock_status}\n\n"
#                 )
#         return products_context
#     def generate_prompt(
#             self,
#             user_name,
#             user_input,
#             products_context,
#             chat_context
#     ):
#         prompt = f"""
# you are a helpful and friendly assistant for {self.company_name} named {self.bot_name}.
# your name is {self.bot_name}.
# you are here to help users with their inquiries and provide information about our products.
# you are not allowed to ask for any personal information from the user.

# current user name: {user_name}.
# Available products and their details:{products_context}

# previous chat history with the user:{chat_context}
# Instructions:
# -always respond in a friendly and helpful manner.
# -provide accurate and relevant information based on the available products and previous chat history.
# -check the stock status of products before providing information to the user.
# -if a product is out of stock, inform the user politely and suggest alternatives if available.
# -be friendly and engaging in your responses, and avoid using technical jargon.
# -focus on being a sales assistant and providing information about the products, rather than engaging in casual conversation.

# user's current input: {user_input}
# """
#         return prompt

#     def chat(
#             self,
#             user_name,
#             user_input,
#             products: List[product],
#             chat_history: List[chathistory]
#     ):
#         products_context = self.get_products_context(products)
#         chat_context = self.get_chat_history_context(chat_history)
#         prompt = self.generate_prompt(
#             user_name,
#             user_input,
#             products_context,
#             chat_context
#         )
#         response = self.get_response(prompt)
#         return response
#     ChatbotService=ChatbotService()