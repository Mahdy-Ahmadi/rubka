import asyncio
import datetime
import json
import re
import logging,os
import uuid
import random
from typing import Any, Callable, Awaitable, Optional, Dict, List, Tuple
from collections import defaultdict, deque


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class StateManager:
    def __init__(self):
        self._states: dict[str, str] = {}
        self._lock = asyncio.Lock()
        logger.info("StateManager initialized.")

    async def set(self, user_id: str, state: str):
        """Sets the state for a given user."""
        async with self._lock:
            self._states[user_id] = state
            logger.debug(f"State set for user {user_id}: {state}")

    async def get(self, user_id: str) -> Optional[str]:
        """Gets the state for a given user."""
        async with self._lock:
            state = self._states.get(user_id)
            logger.debug(f"State get for user {user_id}: {state}")
            return state

    async def clear(self, user_id: str):
        """Clears the state for a given user."""
        async with self._lock:
            if user_id in self._states:
                del self._states[user_id]
                logger.debug(f"State cleared for user {user_id}.")

    async def check(self, user_id: str, state: str) -> bool:
        """Checks if the user's current state matches the given state."""
        async with self._lock:
            user_state = self._states.get(user_id)
            is_match = user_state == state
            logger.debug(f"State check for user {user_id}: expected '{state}', got '{user_state}'. Match: {is_match}")
            return is_match

    async def list_all(self) -> Dict[str, str]:
        """Lists all stored states."""
        async with self._lock:
            logger.debug("Listing all states.")
            return self._states.copy()

    async def get_state_count(self) -> int:
        """Returns the total number of states stored."""
        async with self._lock:
            count = len(self._states)
            logger.debug(f"State count: {count}")
            return count

class DataStorage:
    def __init__(self, file_path: str = "data.json"):
        self.file_path = file_path
        self._data: Dict[str, Any] = {}
        self._lock = asyncio.Lock()

        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                self._data = json.load(f)
                logger.info(f"DataStorage initialized. Loaded data from {self.file_path}.")
        except (FileNotFoundError, json.JSONDecodeError) as e:
            self._data = {}
            logger.warning(f"Data file '{self.file_path}' not found or invalid JSON, starting with empty data. Error: {e}")

    async def set(self, user_id: str, value: Any):
        """Sets a value for a given user ID."""
        async with self._lock:
            self._data[user_id] = value
            await self._async_save()
            logger.debug(f"Data set for user {user_id}.")

    async def get(self, user_id: str) -> Optional[Any]:
        """Gets a value for a given user ID."""
        async with self._lock:
            value = self._data.get(user_id)
            logger.debug(f"Data get for user {user_id}: {'Found' if value is not None else 'Not Found'}")
            return value

    async def delete(self, user_id: str):
        """Deletes a value for a given user ID."""
        async with self._lock:
            if user_id in self._data:
                del self._data[user_id]
                await self._async_save()
                logger.debug(f"Data deleted for user {user_id}.")

    async def _async_save(self):
        """Saves the current data to the file asynchronously."""
        
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, self._save)

    def _save(self):
        """Saves the current data to the file synchronously."""
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(self._data, f, ensure_ascii=False, indent=2)
            logger.debug(f"Data saved to {self.file_path}.")
        except IOError as e:
            logger.error(f"Failed to save data to {self.file_path}: {e}")

    async def get_all_data(self) -> Dict[str, Any]:
        """Returns a copy of all stored data."""
        async with self._lock:
            logger.debug("Getting all data.")
            return self._data.copy()

    async def clear_all_data(self):
        """Clears all stored data and saves the empty state."""
        async with self._lock:
            self._data = {}
            await self._async_save()
            logger.warning("All data cleared from DataStorage.")

class RateLimiter:
    def __init__(self, limit: int = 5, per_seconds: int = 60):
        self.limit = limit
        self.per_seconds = per_seconds
        self._records: Dict[str, deque[datetime.datetime]] = defaultdict(deque)
        self._lock = asyncio.Lock()
        logger.info(f"RateLimiter initialized with limit={limit}, per_seconds={per_seconds}.")

    async def is_allowed(self, user_id: str) -> bool:
        """Checks if a user is allowed to perform an action based on rate limits."""
        async with self._lock:
            now = datetime.datetime.now()
            
            
            while self._records[user_id] and (now - self._records[user_id][0]).total_seconds() >= self.per_seconds:
                self._records[user_id].popleft()
            
            if len(self._records[user_id]) < self.limit:
                self._records[user_id].append(now)
                logger.debug(f"Rate limit allowed for user {user_id}.")
                return True
            else:
                logger.warning(f"Rate limit exceeded for user {user_id}.")
                return False

    async def get_remaining_time(self, user_id: str) -> float:
        """Calculates the time remaining until the user can make another request."""
        async with self._lock:
            now = datetime.datetime.now()
            while self._records[user_id] and (now - self._records[user_id][0]).total_seconds() >= self.per_seconds:
                self._records[user_id].popleft()
            
            if len(self._records[user_id]) < self.limit:
                return 0.0
            else:
                time_since_first_request = now - self._records[user_id][0]
                return max(0.0, self.per_seconds - time_since_first_request.total_seconds())

    async def reset_user_limit(self, user_id: str):
        """Resets the rate limit for a specific user."""
        async with self._lock:
            if user_id in self._records:
                del self._records[user_id]
                logger.info(f"Rate limit reset for user {user_id}.")

class MiddlewareManager:
    def __init__(self):
        self.middlewares: List[Callable[..., Awaitable[bool]]] = []
        logger.info("MiddlewareManager initialized.")

    def add(self, func: Callable[..., Awaitable[bool]]):
        """Adds a middleware function to the manager."""
        self.middlewares.append(func)
        logger.info(f"Middleware '{func.__name__}' added.")

    async def run(self, bot, message) -> bool:
        """Runs all registered middlewares sequentially."""
        logger.debug("Running middlewares.")
        for mw in self.middlewares:
            try:
                result = await mw(bot, message)
                if result is False:
                    logger.debug(f"Middleware '{mw.__name__}' returned False. Stopping middleware chain.")
                    return False
            except Exception as e:
                logger.error(f"Error in middleware '{mw.__name__}': {e}", exc_info=True)
                
                return False 
        logger.debug("All middlewares passed.")
        return True

class CommandParser:
    def __init__(self):
        self.commands: Dict[str, Callable] = {}
        logger.info("CommandParser initialized.")

    def add(self, pattern: str, func: Callable):
        """Adds a command with its regex pattern and handler function."""
        self.commands[pattern] = func
        logger.info(f"Command added: pattern='{pattern}', handler='{func.__name__}'")

    async def run(self, bot, message) -> Optional[Any]:
        """Parses the message text and executes the corresponding command handler."""
        text = message.text or ""
        logger.debug(f"Parsing command for message: '{text[:50]}...'")
        for pattern, func in self.commands.items():
            match = re.match(pattern, text)
            if match:
                try:
                    logger.info(f"Command matched: pattern='{pattern}', handler='{func.__name__}'.")
                    return await func(bot, message, *match.groups())
                except Exception as e:
                    logger.error(f"Error executing command '{func.__name__}' for pattern '{pattern}': {e}", exc_info=True)
                    
                    await message.reply("An error occurred while processing your command.")
                    return None
        logger.debug("No command matched.")
        return None

class Conversation:
    def __init__(self, user_id: str, state_manager: StateManager, conversation_manager: 'ConversationManager'):
        self.user_id = user_id
        self.state_manager = state_manager
        self.conversation_manager = conversation_manager
        self.queue: asyncio.Queue[str] = asyncio.Queue()
        self._is_active = False
        logger.info(f"Conversation created for user {user_id}.")

    async def start(self, initial_state: str):
        """Starts the conversation by setting the initial state."""
        await self.state_manager.set(self.user_id, initial_state)
        self._is_active = True
        logger.info(f"Conversation started for user {self.user_id} with state '{initial_state}'.")

    async def end(self):
        """Ends the conversation and clears the state."""
        await self.state_manager.clear(self.user_id)
        self._is_active = False
        
        while not self.queue.empty():
            try:
                self.queue.get_nowait()
            except asyncio.QueueEmpty:
                pass
        logger.info(f"Conversation ended for user {self.user_id}.")

    async def ask(self, bot, message, text: str) -> Optional[str]:
        """Asks a question to the user and waits for their response."""
        if not self._is_active:
            logger.warning(f"Attempted to ask a question in an inactive conversation for user {self.user_id}.")
            return None
        await message.reply(text)
        try:
            response = await asyncio.wait_for(self.queue.get(), timeout=60.0) 
            logger.debug(f"Received response for user {self.user_id}: '{response}'.")
            return response
        except asyncio.TimeoutError:
            logger.warning(f"Timeout waiting for user {self.user_id}'s response.")
            await self.end()
            return None

    async def next(self, text: str):
        """Puts the user's response into the conversation queue."""
        if not self._is_active:
            logger.warning(f"Attempted to put message in queue for inactive conversation for user {self.user_id}.")
            return
        await self.queue.put(text)
        logger.debug(f"User {self.user_id} response queued.")

    async def is_active(self) -> bool:
        """Checks if the conversation is currently active."""
        return self._is_active

class ConversationManager:
    def __init__(self, state_manager: StateManager):
        self.conversations: Dict[str, Conversation] = {}
        self.state_manager = state_manager
        self._lock = asyncio.Lock()
        logger.info("ConversationManager initialized.")

    async def get_or_create(self, user_id: str) -> Conversation:
        """Gets an existing conversation for a user or creates a new one."""
        async with self._lock:
            if user_id not in self.conversations:
                self.conversations[user_id] = Conversation(user_id, self.state_manager, self)
                logger.debug(f"Created new conversation for user {user_id}.")
            return self.conversations[user_id]

    async def end_conversation(self, user_id: str):
        """Ends a specific user's conversation."""
        async with self._lock:
            if user_id in self.conversations:
                conversation = self.conversations[user_id]
                await conversation.end()
                del self.conversations[user_id]
                logger.info(f"Conversation ended and removed for user {user_id}.")

    async def clean_up_inactive_conversations(self):
        """Removes conversations that are no longer active."""
        async with self._lock:
            users_to_remove = []
            for user_id, conversation in self.conversations.items():
                if not await conversation.is_active():
                    users_to_remove.append(user_id)
            
            for user_id in users_to_remove:
                del self.conversations[user_id]
                logger.info(f"Removed inactive conversation for user {user_id}.")

class Scheduler:
    def __init__(self):
        self.tasks: List[asyncio.Task] = []
        self._running_tasks_lock = asyncio.Lock()
        logger.info("Scheduler initialized.")

    async def run_after(self, delay: int, func: Callable[..., Awaitable[Any]], *args, **kwargs) -> asyncio.Task:
        """Schedules a function to run after a specified delay."""
        async def task():
            await asyncio.sleep(delay)
            try:
                logger.info(f"Running scheduled task '{func.__name__}' after {delay} seconds.")
                await func(*args, **kwargs)
            except Exception as e:
                logger.error(f"Error in scheduled task '{func.__name__}': {e}", exc_info=True)
            finally:
                await self._remove_task_if_completed(asyncio.current_task())

        t = asyncio.create_task(task())
        async with self._running_tasks_lock:
            self.tasks.append(t)
        logger.info(f"Task '{func.__name__}' scheduled to run after {delay} seconds.")
        return t

    async def run_every(self, interval: int, func: Callable[..., Awaitable[Any]], *args, **kwargs) -> asyncio.Task:
        """Schedules a function to run repeatedly at a specified interval."""
        async def task():
            while True:
                await asyncio.sleep(interval)
                try:
                    logger.info(f"Running periodic task '{func.__name__}' every {interval} seconds.")
                    await func(*args, **kwargs)
                except asyncio.CancelledError:
                    logger.info(f"Periodic task '{func.__name__}' cancelled.")
                    break
                except Exception as e:
                    logger.error(f"Error in periodic task '{func.__name__}': {e}", exc_info=True)

        t = asyncio.create_task(task())
        async with self._running_tasks_lock:
            self.tasks.append(t)
        logger.info(f"Task '{func.__name__}' scheduled to run every {interval} seconds.")
        return t

    async def cancel_all_tasks(self):
        """Cancels all scheduled tasks."""
        async with self._running_tasks_lock:
            logger.info(f"Cancelling {len(self.tasks)} scheduled tasks.")
            for task in self.tasks:
                task.cancel()
            
            await asyncio.gather(*self.tasks, return_exceptions=True)
            self.tasks.clear()
            logger.info("All scheduled tasks cancelled.")

    async def _remove_task_if_completed(self, completed_task: asyncio.Task):
        """Removes a completed task from the list of running tasks."""
        async with self._running_tasks_lock:
            if completed_task in self.tasks:
                self.tasks.remove(completed_task)
                logger.debug("Removed a completed task from the scheduler.")

class CacheManager:
    def __init__(self):
        self.cache: Dict[str, Tuple[Any, datetime.datetime]] = {}
        self._lock = asyncio.Lock()
        logger.info("CacheManager initialized.")

    async def get(self, key: str) -> Optional[Any]:
        """Gets a value from the cache, returning None if expired or not found."""
        async with self._lock:
            if key in self.cache:
                value, expire = self.cache[key]
                if expire > datetime.datetime.now():
                    logger.debug(f"Cache hit for key '{key}'.")
                    return value
                else:
                    del self.cache[key]
                    logger.debug(f"Cache expired for key '{key}'.")
            logger.debug(f"Cache miss for key '{key}'.")
            return None

    async def set(self, key: str, value: Any, ttl: int = 300): 
        """Sets a value in the cache with a Time To Live (TTL)."""
        async with self._lock:
            expire = datetime.datetime.now() + datetime.timedelta(seconds=ttl)
            self.cache[key] = (value, expire)
            logger.debug(f"Cache set for key '{key}' with TTL {ttl} seconds.")

    async def delete(self, key: str):
        """Deletes a key from the cache."""
        async with self._lock:
            if key in self.cache:
                del self.cache[key]
                logger.debug(f"Cache deleted for key '{key}'.")

    async def clear(self):
        """Clears all entries from the cache."""
        async with self._lock:
            self.cache.clear()
            logger.warning("Cache cleared.")

    async def prune_expired(self):
        """Removes all expired entries from the cache."""
        async with self._lock:
            now = datetime.datetime.now()
            keys_to_delete = [key for key, (value, expire) in self.cache.items() if expire <= now]
            for key in keys_to_delete:
                del self.cache[key]
            if keys_to_delete:
                logger.debug(f"Pruned {len(keys_to_delete)} expired cache entries.")

class ErrorHandler:
    def __init__(self):
        self.handlers: List[Callable[..., Awaitable[None]]] = []
        logger.info("ErrorHandler initialized.")

    def add(self, func: Callable[..., Awaitable[None]]):
        """Adds an error handler function."""
        self.handlers.append(func)
        logger.info(f"Error handler '{func.__name__}' added.")

    async def run(self, bot, error: Exception, message):
        """Runs all registered error handlers."""
        logger.error(f"An error occurred: {error}", exc_info=True)
        for handler in self.handlers:
            try:
                await handler(bot, error, message)
            except Exception as e:
                logger.error(f"Error in error handler '{handler.__name__}': {e}", exc_info=True)



class LoggerConfigurator:
    """Configures logging levels and formats."""
    def __init__(self, level: int = logging.INFO, format_string: str = '%(asctime)s - %(levelname)s - %(message)s'):
        self.level = level
        self.format_string = format_string
        logger.info("LoggerConfigurator initialized.")

    def configure(self):
        """Applies the logging configuration."""
        logging.basicConfig(level=self.level, format=self.format_string)
        logger.info(f"Logging configured with level {logging.getLevelName(self.level)} and format '{self.format_string}'.")

class UserManager:
    """Manages user data, potentially with more complex profiles."""
    def __init__(self, data_storage: DataStorage):
        self.data_storage = data_storage
        self._lock = asyncio.Lock()
        logger.info("UserManager initialized.")

    async def get_user_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves a user's profile data."""
        profile = await self.data_storage.get(f"profile_{user_id}")
        logger.debug(f"Getting profile for user {user_id}: {'Found' if profile else 'Not Found'}")
        return profile

    async def set_user_profile(self, user_id: str, profile_data: Dict[str, Any]):
        """Sets or updates a user's profile data."""
        await self.data_storage.set(f"profile_{user_id}", profile_data)
        logger.info(f"Profile updated for user {user_id}.")

    async def delete_user_profile(self, user_id: str):
        """Deletes a user's profile data."""
        await self.data_storage.delete(f"profile_{user_id}")
        logger.info(f"Profile deleted for user {user_id}.")

    async def get_all_users(self) -> List[str]:
        """Retrieves a list of all user IDs that have profile data."""
        all_data = await self.data_storage.get_all_data()
        user_ids = [key.replace("profile_", "") for key in all_data if key.startswith("profile_")]
        logger.debug(f"Found {len(user_ids)} users with profiles.")
        return user_ids

class FeatureFlagManager:
    """Manages feature flags to enable/disable features dynamically."""
    def __init__(self, data_storage: DataStorage, default_flags: Optional[Dict[str, bool]] = None):
        self.data_storage = data_storage
        self.default_flags = default_flags or {}
        self._lock = asyncio.Lock()
        logger.info("FeatureFlagManager initialized.")

    async def is_feature_enabled(self, feature_name: str, user_id: Optional[str] = None) -> bool:
        """Checks if a feature is enabled."""
        async with self._lock:
            flag_key = f"feature_flag_{feature_name}"
            stored_flag = await self.data_storage.get(flag_key)

            if stored_flag is not None:
                return stored_flag 
            
            
            if user_id:
                user_flag_key = f"feature_flag_{feature_name}_{user_id}"
                user_specific_flag = await self.data_storage.get(user_flag_key)
                if user_specific_flag is not None:
                    return user_specific_flag

            return self.default_flags.get(feature_name, False) 

    async def enable_feature(self, feature_name: str):
        """Enables a feature globally."""
        await self.data_storage.set(f"feature_flag_{feature_name}", True)
        logger.info(f"Feature '{feature_name}' globally enabled.")

    async def disable_feature(self, feature_name: str):
        """Disables a feature globally."""
        await self.data_storage.set(f"feature_flag_{feature_name}", False)
        logger.info(f"Feature '{feature_name}' globally disabled.")
        
    async def enable_feature_for_user(self, feature_name: str, user_id: str):
        """Enables a feature for a specific user."""
        await self.data_storage.set(f"feature_flag_{feature_name}_{user_id}", True)
        logger.info(f"Feature '{feature_name}' enabled for user {user_id}.")
        
    async def disable_feature_for_user(self, feature_name: str, user_id: str):
        """Disables a feature for a specific user."""
        await self.data_storage.set(f"feature_flag_{feature_name}_{user_id}", False)
        logger.info(f"Feature '{feature_name}' disabled for user {user_id}.")

class MessageQueue:
    """Manages a queue for outgoing messages, useful for rate limiting or batching."""
    def __init__(self, max_size: int = 1000):
        self.queue: deque[Tuple[str, str]] = deque(maxlen=max_size) 
        self._lock = asyncio.Lock()
        self._empty_event = asyncio.Event()
        self._empty_event.set() 
        logger.info(f"MessageQueue initialized with max size {max_size}.")

    async def put(self, user_id: str, message_text: str):
        """Adds a message to the queue."""
        async with self._lock:
            if len(self.queue) < self.queue.maxlen:
                self.queue.append((user_id, message_text))
                self._empty_event.clear() 
                logger.debug(f"Message added to queue for user {user_id}.")
            else:
                logger.warning(f"MessageQueue is full. Could not add message for user {user_id}.")

    async def get(self) -> Optional[Tuple[str, str]]:
        """Gets a message from the queue. Waits if the queue is empty."""
        await self._empty_event.wait() 
        async with self._lock:
            if self.queue:
                user_id, message_text = self.queue.popleft()
                if not self.queue:
                    self._empty_event.set() 
                logger.debug(f"Message retrieved from queue for user {user_id}.")
                return user_id, message_text
            return None

    def is_empty(self) -> bool:
        """Checks if the queue is empty."""
        return not self.queue

    def qsize(self) -> int:
        """Returns the current number of messages in the queue."""
        return len(self.queue)

class TextGenerator:
    """A simple text generator, can be expanded with more sophisticated models."""
    def __init__(self, model_path: Optional[str] = None):
        
        self.model_path = model_path
        if model_path:
            logger.info(f"TextGenerator initialized with model from: {model_path}")
        else:
            logger.info("TextGenerator initialized with basic functionality (no model loaded).")

    async def generate_text(self, prompt: str, max_length: int = 100) -> str:
        """Generates text based on a prompt."""
        
        await asyncio.sleep(0.1) 
        generated_content = f"Generated text based on: '{prompt[:50]}...' (Model: {self.model_path or 'basic'})"
        logger.info(f"Text generated for prompt: '{prompt[:50]}...'")
        return generated_content[:max_length]

class WorkflowEngine:
    """Orchestrates a sequence of steps (tasks) for a given process."""
    def __init__(self):
        self.workflows: Dict[str, List[Callable[..., Awaitable[Any]]]] = {}
        logger.info("WorkflowEngine initialized.")

    def add_workflow(self, name: str, steps: List[Callable[..., Awaitable[Any]]]):
        """Adds a new workflow with a name and a list of step functions."""
        self.workflows[name] = steps
        logger.info(f"Workflow '{name}' added with {len(steps)} steps.")

    async def run_workflow(self, name: str, initial_context: Dict[str, Any]) -> Dict[str, Any]:
        """Runs a workflow and returns the final context."""
        if name not in self.workflows:
            logger.error(f"Workflow '{name}' not found.")
            raise ValueError(f"Workflow '{name}' not found.")
        
        context = initial_context.copy()
        logger.info(f"Running workflow '{name}' with initial context: {context}")
        
        for step_index, step_func in enumerate(self.workflows[name]):
            try:
                logger.debug(f"Executing step {step_index + 1} of workflow '{name}': '{step_func.__name__}'.")
                
                context = await step_func(context)
                logger.debug(f"Step {step_index + 1} completed. Current context: {context}")
            except Exception as e:
                logger.error(f"Error in step {step_index + 1} ('{step_func.__name__}') of workflow '{name}': {e}", exc_info=True)
                
                raise RuntimeError(f"Error in workflow '{name}' step {step_index + 1}: {e}") from e
                
        logger.info(f"Workflow '{name}' completed successfully. Final context: {context}")
        return context

class AnalyticsTracker:
    """Tracks events and metrics for analysis."""
    def __init__(self, data_storage: DataStorage):
        self.data_storage = data_storage
        self._lock = asyncio.Lock()
        logger.info("AnalyticsTracker initialized.")

    async def track_event(self, event_name: str, properties: Optional[Dict[str, Any]] = None):
        """Tracks a specific event with optional properties."""
        timestamp = datetime.datetime.now().isoformat()
        event_data = {"event": event_name, "timestamp": timestamp, "properties": properties or {}}
        
        async with self._lock:
            event_key = f"analytics_event_{timestamp}_{uuid.uuid4().hex[:8]}" 
            await self.data_storage.set(event_key, event_data)
            logger.info(f"Tracked event: '{event_name}' with properties: {properties}")

    async def get_events_by_name(self, event_name: str) -> List[Dict[str, Any]]:
        """Retrieves all tracked events with a specific name."""
        all_data = await self.data_storage.get_all_data()
        matching_events = []
        for key, value in all_data.items():
            if key.startswith("analytics_event_") and isinstance(value, dict) and value.get("event") == event_name:
                matching_events.append(value)
        logger.debug(f"Retrieved {len(matching_events)} events for '{event_name}'.")
        return matching_events

    async def get_all_events(self) -> List[Dict[str, Any]]:
        """Retrieves all tracked events."""
        all_data = await self.data_storage.get_all_data()
        all_events = [value for key, value in all_data.items() if key.startswith("analytics_event_") and isinstance(value, dict)]
        logger.debug(f"Retrieved a total of {len(all_events)} analytics events.")
        return all_events

class NotificationService:
    """Handles sending notifications to users (e.g., push notifications, emails)."""
    def __init__(self, bot_instance):
        self.bot = bot_instance 
        self._lock = asyncio.Lock()
        logger.info("NotificationService initialized.")

    async def send_notification(self, user_id: str, message: str):
        """Sends a notification to a specific user."""
        try:
            
            
            
            await self.bot.send_message(user_id, f"Notification: {message}") 
            logger.info(f"Notification sent to user {user_id}: '{message}'.")
        except Exception as e:
            logger.error(f"Failed to send notification to user {user_id}: {e}", exc_info=True)

    async def broadcast_message(self, user_ids: List[str], message: str):
        """Sends a message to multiple users."""
        async def send_to_user(uid):
            await self.send_notification(uid, message)

        tasks = [send_to_user(uid) for uid in user_ids]
        await asyncio.gather(*tasks, return_exceptions=True)
        logger.info(f"Broadcasted message to {len(user_ids)} users.")

class ConfigurationManager:
    """Loads and manages application configuration from files or environment variables."""
    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        self.config: Dict[str, Any] = {}
        self._lock = asyncio.Lock()
        self._load_config()
        logger.info("ConfigurationManager initialized.")

    def _load_config(self):
        """Loads configuration from a JSON file."""
        try:
            with open(self.config_file, "r", encoding="utf-8") as f:
                self.config = json.load(f)
                logger.info(f"Configuration loaded from '{self.config_file}'.")
        except FileNotFoundError:
            logger.warning(f"Configuration file '{self.config_file}' not found. Using empty configuration.")
            self.config = {}
        except json.JSONDecodeError:
            logger.error(f"Error decoding JSON from configuration file '{self.config_file}'.")
            self.config = {}
        except IOError as e:
            logger.error(f"Error reading configuration file '{self.config_file}': {e}")
            self.config = {}

    async def get(self, key: str, default: Optional[Any] = None) -> Any:
        """Gets a configuration value by key."""
        async with self._lock:
            return self.config.get(key, default)

    async def set(self, key: str, value: Any):
        """Sets a configuration value and saves it to the file."""
        async with self._lock:
            self.config[key] = value
            await self._async_save_config()
            logger.info(f"Configuration updated for key '{key}'.")

    async def _async_save_config(self):
        """Saves the current configuration to the file asynchronously."""
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, self._save_config)

    def _save_config(self):
        """Saves the current configuration to the file synchronously."""
        try:
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
            logger.debug(f"Configuration saved to '{self.config_file}'.")
        except IOError as e:
            logger.error(f"Failed to save configuration to '{self.config_file}': {e}")

class TaskScheduler:
    """A more robust scheduler with capabilities for recurring tasks and monitoring."""
    def __init__(self):
        self.scheduled_tasks: Dict[str, asyncio.Task] = {}
        self._task_id_counter = 0
        self._lock = asyncio.Lock()
        logger.info("TaskScheduler initialized.")

    async def _generate_task_id(self) -> str:
        """Generates a unique task ID."""
        async with self._lock:
            self._task_id_counter += 1
            return f"task_{self._task_id_counter}"

    async def schedule_once(self, delay_seconds: int, func: Callable[..., Awaitable[Any]], *args, **kwargs) -> str:
        """Schedules a task to run once after a delay and returns its ID."""
        task_id = await self._generate_task_id()

        async def task_wrapper():
            await asyncio.sleep(delay_seconds)
            try:
                logger.info(f"Executing one-time task '{func.__name__}' (ID: {task_id}) after {delay_seconds}s.")
                await func(*args, **kwargs)
            except asyncio.CancelledError:
                logger.info(f"One-time task '{func.__name__}' (ID: {task_id}) was cancelled.")
            except Exception as e:
                logger.error(f"Error in one-time task '{func.__name__}' (ID: {task_id}): {e}", exc_info=True)
            finally:
                await self.cancel_task(task_id) 

        task = asyncio.create_task(task_wrapper(), name=f"OneTimeTask_{func.__name__}")
        async with self._lock:
            self.scheduled_tasks[task_id] = task
        logger.info(f"Task '{func.__name__}' (ID: {task_id}) scheduled to run once in {delay_seconds} seconds.")
        return task_id

    async def schedule_recurring(self, interval_seconds: int, func: Callable[..., Awaitable[Any]], *args, **kwargs) -> str:
        """Schedules a task to run recurringly at a given interval and returns its ID."""
        task_id = await self._generate_task_id()

        async def task_wrapper():
            while True:
                try:
                    await asyncio.sleep(interval_seconds)
                    logger.info(f"Executing recurring task '{func.__name__}' (ID: {task_id}) every {interval_seconds}s.")
                    await func(*args, **kwargs)
                except asyncio.CancelledError:
                    logger.info(f"Recurring task '{func.__name__}' (ID: {task_id}) was cancelled.")
                    break 
                except Exception as e:
                    logger.error(f"Error in recurring task '{func.__name__}' (ID: {task_id}): {e}", exc_info=True)
                    

        task = asyncio.create_task(task_wrapper(), name=f"RecurringTask_{func.__name__}")
        async with self._lock:
            self.scheduled_tasks[task_id] = task
        logger.info(f"Task '{func.__name__}' (ID: {task_id}) scheduled to run every {interval_seconds} seconds.")
        return task_id

    async def cancel_task(self, task_id: str) -> bool:
        """Cancels a scheduled task by its ID."""
        async with self._lock:
            if task_id in self.scheduled_tasks:
                task = self.scheduled_tasks[task_id]
                task.cancel()
                try:
                    await task 
                except asyncio.CancelledError:
                    pass 
                del self.scheduled_tasks[task_id]
                logger.info(f"Task with ID '{task_id}' cancelled.")
                return True
            logger.warning(f"Task with ID '{task_id}' not found for cancellation.")
            return False

    async def get_task_status(self, task_id: str) -> str:
        """Gets the status of a scheduled task."""
        async with self._lock:
            if task_id in self.scheduled_tasks:
                task = self.scheduled_tasks[task_id]
                if task.done():
                    return "completed" if not task.cancelled() else "cancelled"
                return "running"
            return "not_found"

    async def get_all_task_ids(self) -> List[str]:
        """Returns a list of all scheduled task IDs."""
        async with self._lock:
            return list(self.scheduled_tasks.keys())

class TokenBucket:
    """Implements a token bucket for rate limiting."""
    def __init__(self, capacity: int, fill_rate: float):
        self.capacity = capacity
        self.fill_rate = fill_rate 
        self.tokens = capacity
        self.last_refill_time = datetime.datetime.now()
        self._lock = asyncio.Lock()
        logger.info(f"TokenBucket initialized with capacity={capacity}, fill_rate={fill_rate}/s.")

    async def _refill_tokens(self):
        """Refills tokens based on the time elapsed since last refill."""
        now = datetime.datetime.now()
        time_elapsed = (now - self.last_refill_time).total_seconds()
        tokens_to_add = time_elapsed * self.fill_rate
        self.tokens = min(self.capacity, self.tokens + tokens_to_add)
        self.last_refill_time = now

    async def consume(self, tokens_needed: float = 1.0) -> bool:
        """Consumes tokens from the bucket. Returns True if successful, False otherwise."""
        async with self._lock:
            await self._refill_tokens()
            if self.tokens >= tokens_needed:
                self.tokens -= tokens_needed
                logger.debug(f"Consumed {tokens_needed} tokens. Remaining: {self.tokens:.2f}")
                return True
            else:
                logger.warning(f"Not enough tokens ({self.tokens:.2f}) to consume {tokens_needed}.")
                return False

class AwaitableQueue:
    """A queue that allows items to be put and retrieved, with ability to signal completion."""
    def __init__(self):
        self.queue: asyncio.Queue[Any] = asyncio.Queue()
        self.completion_signals: Dict[Any, asyncio.Event] = {} 
        self._lock = asyncio.Lock()
        logger.info("AwaitableQueue initialized.")

    async def put(self, item: Any, completion_event: Optional[asyncio.Event] = None):
        """Puts an item into the queue. If completion_event is provided, it will be set when the item is retrieved."""
        await self.queue.put(item)
        if completion_event:
            async with self._lock:
                self.completion_signals[item] = completion_event
        logger.debug(f"Item put into AwaitableQueue.")

    async def get(self) -> Any:
        """Retrieves an item from the queue."""
        item = await self.queue.get()
        completion_event = None
        async with self._lock:
            if item in self.completion_signals:
                completion_event = self.completion_signals.pop(item)
        
        if completion_event:
            completion_event.set()
            logger.debug(f"Item retrieved from AwaitableQueue and completion signal set.")
        else:
            logger.debug(f"Item retrieved from AwaitableQueue.")
        return item
    
    def task_done(self):
        """Indicates that a formerly enqueued task is complete."""
        self.queue.task_done()

    async def join(self):
        """Blocks until all items in the queue have been gotten and processed."""
        await self.queue.join()

class DataValidator:
    """Validates data against predefined schemas or rules."""
    def __init__(self):
        self.schemas: Dict[str, Dict] = {}
        logger.info("DataValidator initialized.")

    def register_schema(self, schema_name: str, schema: Dict):
        """Registers a validation schema."""
        self.schemas[schema_name] = schema
        logger.info(f"Schema '{schema_name}' registered.")

    async def validate(self, data: Any, schema_name: str) -> bool:
        """Validates data against a registered schema."""
        if schema_name not in self.schemas:
            logger.error(f"Schema '{schema_name}' not found for validation.")
            raise ValueError(f"Schema '{schema_name}' not found.")
        
        schema = self.schemas[schema_name]
        
        
        is_valid = True
        if isinstance(schema, dict) and isinstance(data, dict):
            for key, expected_type in schema.items():
                if key not in data:
                    is_valid = False
                    logger.warning(f"Validation failed: Key '{key}' missing in data.")
                    break
                if not isinstance(data[key], expected_type):
                    is_valid = False
                    logger.warning(f"Validation failed: Type mismatch for key '{key}'. Expected {expected_type}, got {type(data[key])}.")
                    break
        else:
            is_valid = False
            logger.warning("Validation failed: Schema or data is not in expected dictionary format.")
        
        logger.info(f"Data validation against schema '{schema_name}': {'Success' if is_valid else 'Failed'}.")
        return is_valid

class IdempotencyManager:
    """Ensures operations are performed only once by tracking request IDs."""
    def __init__(self, storage: DataStorage, expiry_seconds: int = 600):
        self.storage = storage
        self.expiry_seconds = expiry_seconds
        logger.info(f"IdempotencyManager initialized with expiry {expiry_seconds}s.")

    async def is_unique(self, request_id: str) -> bool:
        """Checks if a request ID has been seen before."""
        seen_id = await self.storage.get(f"idempotency_{request_id}")
        return seen_id is None

    async def mark_as_processed(self, request_id: str):
        """Marks a request ID as processed and sets an expiry."""
        await self.storage.set(f"idempotency_{request_id}", True)
        
        
        
        
        
        logger.info(f"Marked request ID '{request_id}' as processed.")

    async def protect(self, request_id: str, func: Callable[..., Awaitable[Any]], *args, **kwargs):
        """Executes a function only if the request ID is unique."""
        if await self.is_unique(request_id):
            result = await func(*args, **kwargs)
            await self.mark_as_processed(request_id)
            return result
        else:
            logger.warning(f"Request ID '{request_id}' is not unique. Operation skipped.")
            return None 

class FileDownloader:
    """Handles downloading files from URLs."""
    def __init__(self, download_dir: str = "downloads"):
        self.download_dir = download_dir
        os.makedirs(self.download_dir, exist_ok=True)
        logger.info(f"FileDownloader initialized. Download directory: '{self.download_dir}'.")

    async def download_file(self, url: str, filename: Optional[str] = None) -> str:
        """Downloads a file from a URL to the specified directory."""
        import aiohttp
        import os
        
        if filename is None:
            filename = url.split('/')[-1]
        filepath = os.path.join(self.download_dir, filename)

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status() 
                with open(filepath, 'wb') as f:
                    while True:
                        chunk = await response.content.read(1024) 
                        if not chunk:
                            break
                        f.write(chunk)
        logger.info(f"File downloaded from {url} to {filepath}.")
        return filepath

class TaskDistributor:
    """Distributes tasks to multiple workers (e.g., for parallel processing)."""
    def __init__(self, num_workers: int):
        self.num_workers = num_workers
        self.task_queue: asyncio.Queue[Tuple[Callable[..., Awaitable[Any]], Tuple, Dict[str, Any]]] = asyncio.Queue()
        self.workers: List[asyncio.Task] = []
        self._workers_running = False
        logger.info(f"TaskDistributor initialized with {num_workers} workers.")

    async def _worker(self, worker_id: int):
        """The function that each worker runs."""
        logger.info(f"Worker {worker_id} started.")
        while True:
            try:
                func, args, kwargs = await self.task_queue.get()
                logger.debug(f"Worker {worker_id} picked up task: {func.__name__}.")
                await func(*args, **kwargs)
                self.task_queue.task_done()
                logger.debug(f"Worker {worker_id} finished task: {func.__name__}.")
            except asyncio.CancelledError:
                logger.info(f"Worker {worker_id} received cancellation signal.")
                break
            except Exception as e:
                logger.error(f"Worker {worker_id} encountered an error: {e}", exc_info=True)
                

    async def start(self):
        """Starts the worker processes."""
        if not self._workers_running:
            self.workers = [
                asyncio.create_task(self._worker(i))
                for i in range(self.num_workers)
            ]
            self._workers_running = True
            logger.info("TaskDistributor workers started.")

    async def stop(self):
        """Stops all worker processes gracefully."""
        if self._workers_running:
            for worker in self.workers:
                worker.cancel()
            await asyncio.gather(*self.workers, return_exceptions=True)
            self._workers_running = False
            logger.info("TaskDistributor workers stopped.")

    async def add_task(self, func: Callable[..., Awaitable[Any]], *args, **kwargs):
        """Adds a task to the queue for workers to process."""
        await self.task_queue.put((func, args, kwargs))
        logger.debug(f"Task '{func.__name__}' added to TaskDistributor queue.")

    async def wait_completion(self):
        """Waits for all tasks currently in the queue to be processed."""
        await self.task_queue.join()
        logger.info("All tasks in TaskDistributor queue have been processed.")

class EventBus:
    """A simple publish-subscribe system."""
    def __init__(self):
        self._subscribers: Dict[str, List[Callable[..., Awaitable[None]]]] = defaultdict(list)
        self._lock = asyncio.Lock()
        logger.info("EventBus initialized.")

    async def subscribe(self, event_name: str, handler: Callable[..., Awaitable[None]]):
        """Subscribes a handler to a specific event."""
        async with self._lock:
            self._subscribers[event_name].append(handler)
        logger.info(f"Handler '{handler.__name__}' subscribed to event '{event_name}'.")

    async def unsubscribe(self, event_name: str, handler: Callable[..., Awaitable[None]]):
        """Unsubscribes a handler from an event."""
        async with self._lock:
            if event_name in self._subscribers and handler in self._subscribers[event_name]:
                self._subscribers[event_name].remove(handler)
                logger.info(f"Handler '{handler.__name__}' unsubscribed from event '{event_name}'.")
            else:
                logger.warning(f"Handler '{handler.__name__}' not found for event '{event_name}' during unsubscription.")

    async def publish(self, event_name: str, *args, **kwargs):
        """Publishes an event, notifying all subscribed handlers."""
        if event_name not in self._subscribers:
            logger.debug(f"No subscribers for event '{event_name}'.")
            return

        handlers = self._subscribers[event_name]
        logger.info(f"Publishing event '{event_name}' to {len(handlers)} subscribers.")
        
        tasks = []
        for handler in handlers:
            tasks.append(asyncio.create_task(handler(*args, **kwargs)))
        
        await asyncio.gather(*tasks, return_exceptions=True)
        logger.debug(f"Event '{event_name}' publishing completed.")

class FileScanner:
    """Scans directories for files based on patterns."""
    def __init__(self, base_dir: str):
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)
        logger.info(f"FileScanner initialized for directory: '{self.base_dir}'.")

    async def find_files(self, pattern: str, recursive: bool = False) -> List[str]:
        """Finds files matching a pattern (glob-style)."""
        import glob
        search_path = os.path.join(self.base_dir, "**" if recursive else "", pattern)
        logger.info(f"Scanning for files with pattern '{pattern}' in '{self.base_dir}' (recursive: {recursive}).")
        
        
        loop = asyncio.get_running_loop()
        found_files = await loop.run_in_executor(None, glob.glob, search_path, recursive=recursive)
        
        logger.info(f"Found {len(found_files)} files matching the pattern.")
        return found_files

    async def read_file_content(self, filepath: str) -> Optional[str]:
        """Reads the content of a given file."""
        if not os.path.isfile(filepath):
            logger.warning(f"File not found for reading: {filepath}")
            return None
        
        try:
            loop = asyncio.get_running_loop()
            with open(filepath, "r", encoding="utf-8") as f:
                content = await loop.run_in_executor(None, f.read)
            logger.debug(f"Read content of file: {filepath}.")
            return content
        except IOError as e:
            logger.error(f"Error reading file '{filepath}': {e}", exc_info=True)
            return None

class WorkerPool:
    """Manages a pool of worker coroutines that process tasks from a queue."""
    def __init__(self, num_workers: int, task_queue: asyncio.Queue):
        self.num_workers = num_workers
        self.task_queue = task_queue
        self.workers: List[asyncio.Task] = []
        self._is_running = False
        logger.info(f"WorkerPool initialized with {num_workers} workers.")

    async def _worker_coro(self, worker_id: int):
        """The coroutine each worker runs."""
        logger.info(f"Worker {worker_id} started.")
        while True:
            try:
                task_payload = await self.task_queue.get()
                logger.debug(f"Worker {worker_id} got task from queue.")
                
                if callable(task_payload):
                    await task_payload()
                else:
                    logger.warning(f"Worker {worker_id} received non-callable task payload: {type(task_payload)}.")
                self.task_queue.task_done()
            except asyncio.CancelledError:
                logger.info(f"Worker {worker_id} cancelled.")
                break
            except Exception as e:
                logger.error(f"Worker {worker_id} error: {e}", exc_info=True)
                

    async def start(self):
        """Starts the worker pool."""
        if not self._is_running:
            self.workers = [asyncio.create_task(self._worker_coro(i)) for i in range(self.num_workers)]
            self._is_running = True
            logger.info("WorkerPool started.")

    async def stop(self):
        """Stops the worker pool gracefully."""
        if self._is_running:
            for worker in self.workers:
                worker.cancel()
            await asyncio.gather(*self.workers, return_exceptions=True)
            self._is_running = False
            logger.info("WorkerPool stopped.")

class DistributedLock:
    """A simple distributed lock implementation (requires a shared backend like Redis or DataStorage)."""
    def __init__(self, storage: DataStorage, lock_name: str, timeout: int = 10):
        self.storage = storage
        self.lock_name = f"lock_{lock_name}"
        self.timeout = timeout 
        self._lock = asyncio.Lock() 
        logger.info(f"DistributedLock initialized for '{lock_name}' with timeout {timeout}s.")

    async def acquire(self, blocking: bool = True, timeout: Optional[float] = None) -> bool:
        """Acquires the lock. Returns True if acquired, False otherwise."""
        effective_timeout = timeout if timeout is not None else self.timeout
        
        async with self._lock:
            start_time = datetime.datetime.now()
            while True:
                acquired = await self.storage.set(self.lock_name, "locked", nx=True, px=int(effective_timeout * 1000)) 
                if acquired:
                    logger.debug(f"Lock '{self.lock_name}' acquired.")
                    return True
                
                if not blocking:
                    logger.debug(f"Lock '{self.lock_name}' could not be acquired (non-blocking).")
                    return False
                
                
                if (datetime.datetime.now() - start_time).total_seconds() > effective_timeout:
                    logger.warning(f"Timeout while trying to acquire lock '{self.lock_name}'.")
                    return False
                
                await asyncio.sleep(0.1) 

    async def release(self) -> bool:
        """Releases the lock."""
        async with self._lock:
            
            
            
            await self.storage.delete(self.lock_name)
            logger.debug(f"Lock '{self.lock_name}' released.")
            return True

    async def __aenter__(self):
        """Context manager entry point for acquiring the lock."""
        if not await self.acquire():
            raise RuntimeError(f"Failed to acquire lock '{self.lock_name}'.")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit point for releasing the lock."""
        await self.release()

class ModelRegistry:
    """Manages a registry of machine learning models."""
    def __init__(self, storage: DataStorage):
        self.storage = storage
        self._registry: Dict[str, Any] = {} 
        self._loaded_models: Dict[str, Any] = {} 
        self._lock = asyncio.Lock()
        logger.info("ModelRegistry initialized.")

    async def register_model(self, model_name: str, model_path_or_instance: Any):
        """Registers a model by name."""
        async with self._lock:
            self._registry[model_name] = model_path_or_instance
            
            if not isinstance(model_path_or_instance, str): 
                self._loaded_models[model_name] = model_path_or_instance
            logger.info(f"Model '{model_name}' registered.")

    async def load_model(self, model_name: str) -> Optional[Any]:
        """Loads a model by name. Caches loaded models."""
        async with self._lock:
            if model_name in self._loaded_models:
                logger.debug(f"Returning cached loaded model: '{model_name}'.")
                return self._loaded_models[model_name]

            if model_name not in self._registry:
                logger.error(f"Model '{model_name}' not found in registry.")
                return None

            model_source = self._registry[model_name]
            
            
            
            
            if isinstance(model_source, str):
                try:
                    
                    
                    loaded_model = f"Loaded_model_from_{model_source}"
                    self._loaded_models[model_name] = loaded_model
                    logger.info(f"Model '{model_name}' loaded from '{model_source}'.")
                    return loaded_model
                except Exception as e:
                    logger.error(f"Failed to load model '{model_name}' from '{model_source}': {e}", exc_info=True)
                    return None
            else: 
                self._loaded_models[model_name] = model_source
                logger.info(f"Model '{model_name}' is an instance and already loaded.")
                return model_source
    
    async def predict(self, model_name: str, data: Any) -> Any:
        """Makes a prediction using a loaded model."""
        model = await self.load_model(model_name)
        if model:
            
            prediction = f"Prediction for {model_name} with data {data}"
            logger.debug(f"Prediction made for model '{model_name}'.")
            return prediction
        return None

class MetricsReporter:
    """Collects and reports application metrics."""
    def __init__(self, storage: DataStorage):
        self.storage = storage
        self._metrics: Dict[str, float] = {}
        self._lock = asyncio.Lock()
        logger.info("MetricsReporter initialized.")

    async def increment_counter(self, metric_name: str, value: float = 1.0):
        """Increments a counter metric."""
        async with self._lock:
            self._metrics[metric_name] = self._metrics.get(metric_name, 0.0) + value
            logger.debug(f"Metric '{metric_name}' incremented by {value}. New value: {self._metrics[metric_name]}.")

    async def set_gauge(self, metric_name: str, value: float):
        """Sets a gauge metric to a specific value."""
        async with self._lock:
            self._metrics[metric_name] = value
            logger.debug(f"Metric '{metric_name}' set to {value}.")

    async def get_metrics(self) -> Dict[str, float]:
        """Returns a snapshot of all current metrics."""
        async with self._lock:
            return self._metrics.copy()

    async def report_metrics(self):
        """Saves the current metrics to storage (e.g., for later analysis)."""
        current_metrics = await self.get_metrics()
        timestamp = datetime.datetime.now().isoformat()
        await self.storage.set(f"metrics_report_{timestamp}", current_metrics)
        logger.info(f"Metrics reported at {timestamp}.")

class StateMachine:
    """Manages complex state transitions."""
    def __init__(self, initial_state: str):
        self.current_state = initial_state
        self.transitions: Dict[Tuple[str, str], Callable[..., Awaitable[None]]] = {}
        self._lock = asyncio.Lock()
        logger.info(f"StateMachine initialized with initial state: '{initial_state}'.")

    def add_transition(self, from_state: str, to_state: str, action: Callable[..., Awaitable[None]]):
        """Adds a transition rule from one state to another, with an optional action."""
        self.transitions[(from_state, to_state)] = action
        logger.info(f"Transition added: '{from_state}' -> '{to_state}' with action '{action.__name__}'.")

    async def transition(self, event: str, *args, **kwargs) -> bool:
        """Triggers a state transition based on an event."""
        async with self._lock:
            potential_next_state = None
            action = None

            
            
            
            
            
            

            
            
            
            
            
            
            
            
            

            
            

            
            
            
            
            possible_transitions = [(fs, ts) for fs, ts in self.transitions.keys() if fs == self.current_state]
            
            found_transition = False
            for fs, ts in possible_transitions:
                
                
                if event == ts: 
                    potential_next_state = ts
                    action = self.transitions[(fs, ts)]
                    found_transition = True
                    break
            
            if found_transition:
                logger.info(f"Transitioning from '{self.current_state}' to '{potential_next_state}' on event '{event}'.")
                if action:
                    await action(*args, **kwargs)
                self.current_state = potential_next_state
                logger.info(f"Current state is now: '{self.current_state}'.")
                return True
            else:
                logger.warning(f"No valid transition found from state '{self.current_state}' on event '{event}'.")
                return False

    async def get_state(self) -> str:
        """Gets the current state."""
        async with self._lock:
            return self.current_state

class RoleBasedAccessControl:
    """Manages user roles and permissions."""
    def __init__(self, storage: DataStorage):
        self.storage = storage
        self._roles: Dict[str, List[str]] = {} 
        self._permissions: Dict[str, List[str]] = {} 
        self._lock = asyncio.Lock()
        logger.info("RoleBasedAccessControl initialized.")

    async def add_role_to_user(self, user_id: str, role: str):
        """Assigns a role to a user."""
        async with self._lock:
            if user_id not in self._roles:
                self._roles[user_id] = []
            if role not in self._roles[user_id]:
                self._roles[user_id].append(role)
                await self._save_roles()
                logger.info(f"Role '{role}' assigned to user {user_id}.")

    async def remove_role_from_user(self, user_id: str, role: str):
        """Removes a role from a user."""
        async with self._lock:
            if user_id in self._roles and role in self._roles[user_id]:
                self._roles[user_id].remove(role)
                await self._save_roles()
                logger.info(f"Role '{role}' removed from user {user_id}.")

    async def define_role_permissions(self, role: str, permissions: List[str]):
        """Defines the permissions for a specific role."""
        async with self._lock:
            self._permissions[role] = permissions
            await self._save_permissions()
            logger.info(f"Permissions defined for role '{role}': {permissions}.")

    async def user_has_permission(self, user_id: str, required_permission: str) -> bool:
        """Checks if a user has a specific permission."""
        async with self._lock:
            user_roles = self._roles.get(user_id, [])
            for role in user_roles:
                role_permissions = self._permissions.get(role, [])
                if required_permission in role_permissions:
                    logger.debug(f"User {user_id} has permission '{required_permission}' via role '{role}'.")
                    return True
            logger.debug(f"User {user_id} does NOT have permission '{required_permission}'.")
            return False

    async def _save_roles(self):
        """Saves the current role assignments."""
        await self.storage.set("rbac_roles", self._roles)

    async def _save_permissions(self):
        """Saves the current role permissions."""
        await self.storage.set("rbac_permissions", self._permissions)

    async def load_from_storage(self):
        """Loads roles and permissions from storage."""
        async with self._lock:
            roles_data = await self.storage.get("rbac_roles")
            if roles_data:
                self._roles = roles_data
                logger.info("RBAC roles loaded from storage.")
            perms_data = await self.storage.get("rbac_permissions")
            if perms_data:
                self._permissions = perms_data
                logger.info("RBAC permissions loaded from storage.")


class MockMessage:
    def __init__(self, text: str = "", user_id: str = "test_user", chat_id: str = "test_chat"):
        self.text = text
        self.from_user = type('User', (object,), {'id': user_id})()
        self.chat = type('Chat', (object,), {'id': chat_id})()

    async def reply(self, text: str):
        print(f"Mock Reply to {self.from_user.id}: {text}")
        await asyncio.sleep(0.01) 

