# Space Voyage

A 3D space navigation game where you pilot your spacecraft through a treacherous journey back to Earth.

## About

Space Voyage is a first-person space flight game. You've been on an 8-year mission and must now navigate your spacecraft home through a dangerous path filled with space debris. Traveling at 16.18% the speed of light, even a tiny piece of dust could be fatal.

To help you return safely, a **Safety Tunnel** has been created, marked by large **blue gates**. Stay within these gates to survive. Venture outside, and it's instant death.

The closer you get to Earth, the stronger the gravitational force becomes, making navigation increasingly challenging.

## Pages

### Index (index.html)
The main entry point and home screen of the game. Features:
- Welcome screen with game introduction
- Story background from "Amiral Casanova"
- Graphic settings selection (Low, Medium, High)
- 3D WebGL visualization

### Difficulty Levels
Choose your graphic quality based on your device's capabilities:
- **Low (low.html)** - Optimized for lower-end devices
- **Medium (medium.html)** - Balanced performance and visuals
- **High (high.html)** - Best visual quality for powerful devices

All difficulty levels offer the same gameplay with different graphic fidelity.

### Leaderboard (leaderBoard.html)
View the top 50 players worldwide:
- Player names
- Gates passed
- Time in game
- Firebase-powered global rankings
- Quick access to replay any difficulty level

### Mobile (mobile.html)
Optimized for touch devices:
- Touch controls (tap top, bottom, left, right to navigate)
- Mobile-specific interface
- Same core gameplay adapted for touchscreens
- Access to leaderboard after game over

## Gameplay

- Navigate through blue safety gates
- Avoid space debris at all costs
- Manage gravitational forces as you approach Earth
- Survive as long as possible and climb the leaderboard

## Technology

- Built with Three.js for 3D rendering
- Firebase for leaderboard data and persistence
- Responsive design for desktop and mobile
- Progressive enhancement based on device capabilities
