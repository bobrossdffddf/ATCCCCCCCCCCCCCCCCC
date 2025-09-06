# ATC Training Discord Bot

## Overview

This is a Discord bot designed for Air Traffic Control (ATC) training simulations. The bot presents realistic ATC scenarios to users through interactive Discord messages with multiple-choice options. Users can practice making correct ATC decisions and receive immediate feedback on their choices. The bot manages training sessions, tracks user progress, and provides explanations for correct answers to help users learn proper ATC procedures and communication protocols.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Bot Framework
- **Discord.py**: Uses the discord.py library with the commands extension for creating Discord bot functionality
- **Command Prefix**: Uses "!" as the command prefix for bot interactions
- **Intents**: Configured with default Discord intents for basic bot operations

### Session Management
- **User Sessions**: Implements in-memory session tracking using a `user_sessions` dictionary to manage individual user training progress
- **Session State**: Tracks current scenario index, user progress, and session data for each active user
- **Session Isolation**: Ensures users can only interact with their own training sessions through user ID validation

### Scenario System
- **JSON Storage**: Scenarios are stored in a `scenarios.json` file for easy management and modification
- **Dynamic Loading**: Scenarios are loaded at startup and can be modified without code changes
- **Scenario Structure**: Each scenario includes:
  - Unique ID for tracking
  - Realistic ATC scenario description
  - Multiple choice options (typically 3 options)
  - Correct answer index
  - Educational explanation for the correct choice

### Interactive UI Components
- **Discord UI Buttons**: Utilizes Discord's UI framework with custom button components (`ATCButton` class)
- **Button Styling**: Uses primary button style for consistent visual appearance
- **Dynamic Button Generation**: Creates buttons dynamically based on scenario options
- **User Validation**: Implements callback validation to ensure only the session owner can interact with buttons

### Data Persistence
- **File-based Storage**: Uses JSON file format for scenario persistence
- **Load/Save Functions**: Implements utility functions for reading and writing scenario data
- **Error Handling**: Includes basic file existence checking and JSON parsing

### Environment Configuration
- **Environment Variables**: Uses python-dotenv for managing sensitive configuration
- **Token Security**: Discord bot token is stored securely in environment variables
- **Startup Validation**: Validates required environment variables at startup

## External Dependencies

### Core Libraries
- **discord.py**: Discord API wrapper for bot functionality and real-time messaging
- **python-dotenv**: Environment variable management for secure configuration

### Discord Platform
- **Discord API**: Primary platform for bot deployment and user interaction
- **Discord Webhooks**: For message sending and receiving user interactions
- **Discord UI Framework**: For interactive buttons and user interface components

### File System
- **Local JSON Storage**: Scenario data stored in local `scenarios.json` file
- **Environment File**: `.env` file for storing sensitive configuration data

### Runtime Environment
- **Python 3.x**: Core runtime environment
- **File I/O Operations**: For reading/writing JSON scenario data and environment configuration