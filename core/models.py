# ============================================================
# IMPORTS
# ============================================================

from django.db import models
from django.contrib.auth.models import User


# ============================================================
# 1. LISTING MODEL
# ============================================================
# This model stores the items that students post on CampusLoop.
#
# Example:
# A student wants to sell a Python book.
#
# The listing stores:
# - Who is selling it
# - Item title
# - Description
# - Category
# - Condition
# - Price
# - Exchange type
# - Availability
# - Date it was posted
# ============================================================

class Listing(models.Model):

    # --------------------------------------------------------
    # SELLER
    # --------------------------------------------------------
    # Student who owns/sells the item.

    seller = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='listings'
    )

    # --------------------------------------------------------
    # ITEM TITLE
    # --------------------------------------------------------
    # Example:
    # "Python Programming Book"

    title = models.CharField(
        max_length=200
    )

    # --------------------------------------------------------
    # DESCRIPTION
    # --------------------------------------------------------
    # Detailed information about the item.

    description = models.TextField()

    # --------------------------------------------------------
    # CATEGORY
    # --------------------------------------------------------
    # Example:
    # Book, Electronics, Clothing, Other

    category = models.CharField(
        max_length=100
    )

    # --------------------------------------------------------
    # CONDITION
    # --------------------------------------------------------
    # Example:
    # New, Good, Used

    condition = models.CharField(
        max_length=50
    )

    # --------------------------------------------------------
    # PRICE
    # --------------------------------------------------------
    # Example:
    # ₹300

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    # --------------------------------------------------------
    # EXCHANGE TYPE
    # --------------------------------------------------------
    # Example:
    # Sell, Swap, Borrow, Give

    exchange_type = models.CharField(
        max_length=20
    )

    # --------------------------------------------------------
    # AVAILABILITY
    # --------------------------------------------------------
    # True  = Item is available
    # False = Item has been sold / completed
    #
    # New listings automatically start as available.

    is_available = models.BooleanField(
        default=True
    )

    # --------------------------------------------------------
    # CREATED DATE
    # --------------------------------------------------------
    # Automatically stores when the listing was created.

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    # --------------------------------------------------------
    # DISPLAY NAME IN DJANGO ADMIN
    # --------------------------------------------------------

    def __str__(self):
        return self.title


# ============================================================
# 2. ITEM REQUEST MODEL
# ============================================================
# This model stores formal requests made for a listing.
#
# NOTE:
# This is separate from the direct Message/Chat system.
# Normal student-to-student communication uses Message.
# ============================================================

class ItemRequest(models.Model):

    # --------------------------------------------------------
    # LISTING
    # --------------------------------------------------------
    # The item for which the request was created.

    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE
    )

    # --------------------------------------------------------
    # REQUESTER
    # --------------------------------------------------------
    # Student who created the request.

    requester = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    # --------------------------------------------------------
    # REQUEST MESSAGE
    # --------------------------------------------------------
    # Message written with the request.

    message = models.TextField()

    # --------------------------------------------------------
    # REQUEST STATUS
    # --------------------------------------------------------
    # Example:
    # Pending, Accepted, Rejected

    status = models.CharField(
        max_length=20,
        default='Pending'
    )

    # --------------------------------------------------------
    # CREATED DATE
    # --------------------------------------------------------

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    # --------------------------------------------------------
    # DISPLAY NAME IN DJANGO ADMIN
    # --------------------------------------------------------

    def __str__(self):
        return f"Request for {self.listing.title}"


# ============================================================
# 3. MESSAGE MODEL
# ============================================================
# This is the MAIN DIRECT CHAT SYSTEM of CampusLoop.
#
# Flow:
#
# Student
#    ↓
# Contact Seller
#    ↓
# Message
#    ↓
# Seller's Inbox
#    ↓
# Conversation
#
# Admin is NOT involved in this communication.
# ============================================================

class Message(models.Model):

    # --------------------------------------------------------
    # LISTING
    # --------------------------------------------------------
    # The item related to this conversation.

    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name='messages'
    )

    # --------------------------------------------------------
    # SENDER
    # --------------------------------------------------------
    # Student who sends the message.

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )

    # --------------------------------------------------------
    # RECEIVER
    # --------------------------------------------------------
    # Student who receives the message.

    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_messages'
    )

    # --------------------------------------------------------
    # MESSAGE TEXT
    # --------------------------------------------------------
    # Actual message.
    #
    # Example:
    # "Hi, is this book still available?"

    text = models.TextField()

    # --------------------------------------------------------
    # READ STATUS
    # --------------------------------------------------------
    # False = Unread
    # True  = Read
    #
    # Used for the NEW indicator in Inbox.

    is_read = models.BooleanField(
        default=False
    )

    # --------------------------------------------------------
    # CREATED DATE
    # --------------------------------------------------------
    # Automatically stores when the message was sent.

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    # --------------------------------------------------------
    # DISPLAY NAME IN DJANGO ADMIN
    # --------------------------------------------------------

    def __str__(self):
        return f"{self.sender.username} → {self.receiver.username}"