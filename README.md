# what-to-code
A clone of https://what-to-code.com/. Built with Flask, Html, and CSS

## Overview
This website was made to practice my web development skills. I am trying to replicate every feature of the website stated in the decription:

- [x] submit coding ideas.
- [x] get a random idea.
- [ ] display a dynamically loaded list of all ideas.
- [x] sort ideas by popularity and time.
- [x] filter ideas with specific tags.
- [x] let users like posts anonymously.
- [ ] a similar UI to the original website.

Extras:

- [ ] create an API for the website.

## Submit coding ideas
I achieved this by creating a form that when submitted, sent a POST request to the same page. The python flask backend would then get the form title, description and tags from the form. It would then cleanse the tag data by removing spaces from each tag, and storing the post and tag data in an sqlite database, then redirecting to the home page

## Get a random idea
This was achieved by simply using python to pick a random post from a list of posts and displaying it

## Sort ideas by popularity and time.
This was achieved by parsing arguments in the URL of the request.

For example, the URL: `https://what-to-code.com/?order=RISING` would be read by flask which would fetch posts from the database as requested by the user by using the `order` parameter.

## Filter ideas by specifc tags
This was achieved in the same way as populariy and time sorting. If no tag is passed, Flask will look for posts with "all" tag.

Every post is given the "all" tag when it is made.

### Let users like posts anonymously.
This was done by creating an encrypted cookie which stores every post the user has liked. When a post is liked, a POST request is sent to the like route via javascript. This is done via javascript to avoid page refresh to provide a better user experience.

When Flask recieves the post request, it checks if the post id exists in the users liked posts cookie. If it does, it will decrease the number of likes in the post, and if it doesn't it will increase the number of likes. It then returns json which contains data about the number of likes of the post, and whether or not the user has liked it. This json data is read by the javascript code and used to update the number of likes, as well as the like icon and if it should be filled in or not.

I am aware this system has its flaws, allowing users to abuse the number of likes a post has by deleting cookie data. However this is the approach the original site takes, and the approach I would take because of the convenience to the end user and how insignifcant the number of likes on a post is, on a site such as this.



