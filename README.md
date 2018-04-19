# cover_learner
This project aims to utilise Keras to identify trends in video game cover art. The work is inspired by <a href="https://arxiv.org/abs/1610.09204"><i>Judging a book by its Cover</i></a> by Iwana et. al. Ideally, I want to see if there are any common themes amongst games which have high scores compared to games which have low scores.

I'm using this project as a means to learn more about Keras, Github and Python.

My current version utilising data augmentation is capable of classifying with about 44% accuracy. An example of some of the possible groupings is presented:

![alt text](https://github.com/dkersh/cover_learner/blob/master/examples.png)

More work needs to be done to understand what kinds of features the CNN is picking out however. (Duplicate images are most likely due to games being multi-platform. I'll have to rectify some code to fix this).
