# Translating Of The Dead
An English-French translating game

This project was made at SLAM Hacks, April 2-3 2016.

## Inspiration
I took French in school for most of my life, but once university started I had little opportunity to practice. I try to use French when I can, but I need to try to keep my vocabulary fresh. There are many apps out there that help with vocabulary, but most of them are extremely boring and act like virtual flash cards. I wanted to turn the boring part of language learning into a fun game.

## What it does
This game is based off of Typing of the Dead, a game where zombies swarm the player who must type out words to kill them. In this case, players must type out the English or French translation of the words to slay the enemies. The words are loaded from a text file (words.txt), and enemies will carry either the English or French version of the word (randomly assigned). 
Enemies spawn around the edges of the window and move towards the player's house. The player loses if one of the enemies reaches the house, and the player progresses through the levels by slaying the required amount of enemies. Each successive level increases the enemy spawn rate, average enemy speed, and max amount of enemies for the level. The game does not end, but it does keep track of the highest score.

## How we built it
This game was written in Python, using the Pygame framework. Pygame is a wrapper for the SDL library designed for writing games and is highly portable.

## Challenges we ran into
I have never written a game before, so this whole hackathon was a big learning experience. I've been using Python for a long time now, and Pygame seemed like an easy choice for implementing the game. Since it was my first time though, I ran into a bunch of problems with simply getting things working. The movement of the enemies towards the house was hard to smooth out, and I am still not completely happy with the result. Setting up the sprites and orienting them correctly took a lot of trial and error as well.

## Accomplishments that I'm proud of
I'm honestly very happy with the end result. I had no idea what I was doing when I started, but I managed to actually produce a working version of the game.

## What I learned
This hackathon made me love Python even more. I learned how easy it is to build games using Pygame, and I look forward to making more in the future.

## What's next for Translating of the Dead
I would like to make this game modular, allowing for word banks of different languages to be used. Additionally I would love to add sound and music to the game. Maybe in the future I could port this to be used as a web application.