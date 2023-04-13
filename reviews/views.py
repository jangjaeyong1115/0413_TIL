from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Review, Comment
from .forms import ReviewForm, CommentForm

# Create your views here.

def index(request):
    reviews = Review.objects.all()
    context = {
        'reviews' : reviews,
    }

    return render(request, 'reviews/index.html', context)

def detail(request, pk):
    review = Review.objects.get(pk=pk)
    comment_form = CommentForm()

    comments = review.comment_set.all()
    context = {
        'review' : review,
        'comment_form' : comment_form,
        'comments' : comments,
    }

    return render(request, 'reviews/detail.html', context)

def create(request):
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('reviews:detail', review.pk)
        
    else:
        form = ReviewForm()

    context = {
        'form' : form,
    }

    return render(request,'reviews/create.html', context)


def delete(request, review_pk):
    review = Review.objects.get(pk=review_pk)
    if request.user == review.user:
        review.delete()
    return redirect('reviews:index')

def update(request, review_pk):
    review = Review.objects.get(pk=review_pk)
    if request.user == review.user:
        if request.method == 'POST':
            form = ReviewForm(request.POST, instance=review)
            if form.is_valid():
                form.save()
                return redirect('reviews:detail', review.pk)
            else:
                form = ReviewForm(instance=review)
        else:
            return redirect('reviews:index')

    context = {
        'review': review,
        'form': form,
    }
    return render(request, 'reviews/update.html', context)

def comment_create(request, review_pk):
    # 몇 번 게시글인지 조회
    review = Review.objects.get(pk=review_pk)
    # 댓글 데이터를 받아서
    comment_form = CommentForm(request.POST)
    # 유효성 검증
    if comment_form.is_valid():
        # commit을 False로 지정하면 인스턴스는 반환하면서도 DB에 레코드는 작성하지 않도록 함
        comment = comment_form.save(commit=False)
        comment.review = review
        comment.user = request.user
        comment.save()
        return redirect('reviews:detail', review.pk)
    context = {
        'review': review,
        'comment_form': comment_form,
    }
    return render(request, 'reviews/detail.html', context)

@login_required
def comment_delete(request, review_pk, comment_pk):
    # 삭제할 댓글을 조회
    comment = Comment.objects.get(pk=comment_pk)
    # article_pk = comment.article.pk
    # 댓글 삭제
    if request.user == comment.user:

        comment.delete()
    return redirect('reviews:detail', review_pk)
