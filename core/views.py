from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q

from .models import Listing, ItemRequest, Message
from .forms import ListingForm, ItemRequestForm


# =========================================================
# HOME
# =========================================================

def home(request):
    listings = Listing.objects.filter(
        is_available=True
    ).order_by('-created_at')[:6]

    return render(
        request,
        'core/home.html',
        {
            'listings': listings
        }
    )


# =========================================================
# BROWSE LISTINGS
# =========================================================

def listings(request):

    # IMPORTANT:
    # Show ALL listings here.
    # Sold items should NOT disappear from Browse.
    items = Listing.objects.all().order_by('-created_at')

    search = request.GET.get('search', '').strip()
    category = request.GET.get('category', '').strip()
    exchange_type = request.GET.get('exchange_type', '').strip()

    # Search
    if search:
        items = items.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search) |
            Q(category__icontains=search)
        )

    # Category filter
    if category:
        items = items.filter(
            category__iexact=category
        )

    # Exchange type filter
    if exchange_type:
        items = items.filter(
            exchange_type__iexact=exchange_type
        )

    return render(
        request,
        'core/listings.html',
        {
            'items': items,
            'search': search,
            'category': category,
            'exchange_type': exchange_type,
        }
    )


# =========================================================
# ADD LISTING
# =========================================================

@login_required
def add_listing(request):

    if request.method == 'POST':

        form = ListingForm(request.POST)

        if form.is_valid():

            listing = form.save(commit=False)

            # Logged-in student becomes the seller
            listing.seller = request.user

            # New item is available by default
            listing.is_available = True

            listing.save()

            return redirect(
                'listing_detail',
                id=listing.id
            )

    else:
        form = ListingForm()

    return render(
        request,
        'core/add_listing.html',
        {
            'form': form
        }
    )


# =========================================================
# LISTING DETAIL
# =========================================================

def listing_detail(request, id):

    item = get_object_or_404(
        Listing,
        id=id
    )

    request_form = ItemRequestForm()

    # =====================================================
    # ITEM REQUEST
    # =====================================================

    if request.method == 'POST':

        # User must be logged in
        if not request.user.is_authenticated:
            return redirect(
                f'/login/?next=/listings/{item.id}/'
            )

        # Seller cannot request own item
        if item.seller == request.user:
            return redirect(
                'listing_detail',
                id=item.id
            )

        # Sold item cannot receive new requests
        if not item.is_available:
            return redirect(
                'listing_detail',
                id=item.id
            )

        request_form = ItemRequestForm(
            request.POST
        )

        if request_form.is_valid():

            item_request = request_form.save(
                commit=False
            )

            item_request.listing = item
            item_request.requester = request.user
            item_request.status = 'Pending'

            item_request.save()

            return redirect(
                'my_requests'
            )

    return render(
        request,
        'core/listing_detail.html',
        {
            'item': item,
            'request_form': request_form,
        }
    )


# =========================================================
# REGISTER
# =========================================================

def register(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':

        username = request.POST.get(
            'username',
            ''
        ).strip()

        password = request.POST.get(
            'password',
            ''
        )

        confirm_password = request.POST.get(
            'confirm_password',
            ''
        )

        error = None

        if not username:

            error = 'Username is required.'

        elif not password:

            error = 'Password is required.'

        elif password != confirm_password:

            error = 'Passwords do not match.'

        elif User.objects.filter(
            username=username
        ).exists():

            error = 'Username already exists.'

        if error:

            return render(
                request,
                'core/register.html',
                {
                    'error': error,
                    'username': username,
                }
            )

        user = User.objects.create_user(
            username=username,
            password=password
        )

        login(
            request,
            user
        )

        return redirect('home')

    return render(
        request,
        'core/register.html',
        {
            'username': '',
        }
    )


# =========================================================
# CONTACT SELLER
# =========================================================

@login_required
def contact_seller(request, id):

    item = get_object_or_404(
        Listing,
        id=id
    )

    # Listing must have a seller
    if not item.seller:

        return redirect(
            'listing_detail',
            id=item.id
        )

    # Seller cannot contact themselves
    if request.user == item.seller:

        return redirect(
            'listing_detail',
            id=item.id
        )

    # Sold items cannot be contacted
    if not item.is_available:

        return redirect(
            'listing_detail',
            id=item.id
        )

    # Open direct conversation with seller
    return redirect(
        'conversation',
        id=item.id,
        user_id=item.seller.id
    )


# =========================================================
# INBOX
# =========================================================

@login_required
def inbox(request):

    # Get messages where current user is either
    # sender OR receiver
    all_messages = Message.objects.filter(
        Q(sender=request.user) |
        Q(receiver=request.user)
    ).select_related(
        'listing',
        'sender',
        'receiver'
    ).order_by(
        '-created_at'
    )

    conversations = {}

    for message in all_messages:

        # Determine the other student
        if message.sender_id == request.user.id:

            other_user = message.receiver

        else:

            other_user = message.sender

        # Never show self-conversation
        if other_user.id == request.user.id:
            continue

        # One conversation is identified by:
        # listing + other student
        key = (
            message.listing_id,
            other_user.id
        )

        # Because messages are newest first,
        # the first message is the latest one.
        if key not in conversations:

            conversations[key] = {
                'message': message,
                'other_user': other_user,
                'unread': (
                    message.receiver_id == request.user.id
                    and not message.is_read
                )
            }

    conversation_list = list(
        conversations.values()
    )

    return render(
        request,
        'core/inbox.html',
        {
            'conversations': conversation_list
        }
    )


# =========================================================
# CONVERSATION
# =========================================================

@login_required
def conversation(request, id, user_id):

    item = get_object_or_404(
        Listing,
        id=id
    )

    other_user = get_object_or_404(
        User,
        id=user_id
    )

    # Cannot talk to yourself
    if request.user.id == other_user.id:

        return redirect('inbox')

    # A conversation for a listing is valid when either the logged-in user
    # is the seller or the seller is the other participant in the chat.
    # This allows buyers to open a direct chat with the seller while keeping
    # conversations restricted to the listing's participants.
    if request.user != item.seller and other_user != item.seller:

        return redirect('inbox')

    # =====================================================
    # MARK MESSAGES AS READ
    # =====================================================

    Message.objects.filter(
        listing=item,
        sender=other_user,
        receiver=request.user,
        is_read=False
    ).update(
        is_read=True
    )

    # =====================================================
    # SEND MESSAGE
    # =====================================================

    if request.method == 'POST':

        text = request.POST.get(
            'text',
            ''
        ).strip()

        if text:

            Message.objects.create(
                listing=item,
                sender=request.user,
                receiver=other_user,
                text=text,
                is_read=False
            )

        return redirect(
            'conversation',
            id=item.id,
            user_id=other_user.id
        )

    # =====================================================
    # GET MESSAGES BETWEEN THESE TWO USERS
    # =====================================================

    messages = Message.objects.filter(
        listing=item
    ).filter(
        Q(
            sender=request.user,
            receiver=other_user
        )
        |
        Q(
            sender=other_user,
            receiver=request.user
        )
    ).select_related(
        'sender',
        'receiver'
    ).order_by(
        'created_at'
    )

    return render(
        request,
        'core/conversation.html',
        {
            'item': item,
            'other_user': other_user,
            'messages': messages,
        }
    )


# =========================================================
# LOGOUT
# =========================================================

@login_required
def logout_user(request):

    if request.method == 'POST':

        logout(request)

    return redirect('home')


# =========================================================
# DASHBOARD
# =========================================================

@login_required
def dashboard(request):

    my_listings = Listing.objects.filter(
        seller=request.user
    ).order_by(
        '-created_at'
    )

    return render(
        request,
        'core/dashboard.html',
        {
            'my_listings': my_listings
        }
    )


# =========================================================
# MY REQUESTS
# =========================================================

@login_required
def my_requests(request):

    requests = ItemRequest.objects.filter(
        requester=request.user
    ).select_related(
        'listing',
        'listing__seller'
    ).order_by(
        '-created_at'
    )

    return render(
        request,
        'core/my_requests.html',
        {
            'requests': requests
        }
    )


# =========================================================
# MARK ITEM AS SOLD
# =========================================================

@login_required
def mark_as_sold(request, id):

    item = get_object_or_404(
        Listing,
        id=id
    )

    # Only owner/seller can mark item as sold
    if item.seller != request.user:

        return redirect(
            'dashboard'
        )

    item.is_available = False

    item.save(
        update_fields=[
            'is_available'
        ]
    )

    return redirect(
        'dashboard'
    )