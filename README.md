# Space Voyage

A 3D space navigation game where you pilot a spacecraft through a safety tunnel at 16.18% the speed of light.

## About

Space Voyage is a first-person space flight game. After an 8-year mission, you must navigate your spacecraft safely back home through a dangerous field of invisible space debris. A safety tunnel marked by blue gates provides the only safe path - stray outside and it's instant death!

The game features:
- Increasing gravitational force as you approach home
- Three difficulty levels with varying graphics quality
- Online leaderboard to compete with other players
- Mobile touch controls for on-the-go gaming

## Pages

### index.html
The main entry point and home screen. Features:
- Welcome screen with game introduction
- Graphic settings selection (Low, Medium, High)
- Story introduction from Admiral Casanova

### low.html
Low graphics quality game mode. Best for older devices or when performance is a concern.

### medium.html
Medium graphics quality game mode. Balanced option for most devices.

### high.html
High graphics quality game mode. Best visual experience for powerful devices.

### leaderBoard.html
Online leaderboard showing top 50 players. Features:
- Player names
- Gates passed
- Time in game
- Quick access buttons to restart at any difficulty level

### mobile.html
Mobile-optimized version with touch controls:
- Tap top/bottom/left/right areas to navigate
- Same gameplay as desktop versions
- Optimized for touch devices

## Technology

- **3D Engine**: Three.js
- **Animation**: GSAP (TweenMax)
- **Backend**: Firebase Firestore (for leaderboard data)
- **Styling**: Custom CSS with responsive design

## How to Play

1. Start at the index page and select your graphics quality
2. Read the instructions from Admiral Casanova
3. Use arrow keys (or touch controls on mobile) to navigate through the blue gates
4. Avoid hitting the tunnel walls or going outside the safety zone
5. Try to pass through as many gates as possible
6. Submit your score to the leaderboard when your run ends

## Controls

- **Desktop**: Arrow keys to move
- **Mobile**: Tap the directional touch areas (top, bottom, left, right)
