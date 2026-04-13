"""
cloud_sync_manager.py - Batches cloud updates to reduce API calls
Instead of syncing every fact, batch updates and sync periodically
"""
import time

class CloudSyncManager:
    def __init__(self, sync_interval=30, batch_size=10):
        self.sync_interval = sync_interval  # seconds between syncs
        self.batch_size = batch_size  # facts to accumulate before sync
        self.last_sync = time.time()
        self.pending_updates = {
            "facts": [],
            "emotions": [],
            "preferences": {}
        }
        self.sync_history = []

    def queue_fact(self, fact):
        """Add a fact to the sync queue"""
        self.pending_updates["facts"].append(fact)

    def queue_emotion(self, emotion):
        """Add an emotion to the sync queue"""
        self.pending_updates["emotions"].append(emotion)

    def queue_preference(self, key, value):
        """Queue a preference update"""
        self.pending_updates["preferences"][key] = value

    def should_sync(self):
        """Check if we should sync now"""
        # Sync if batch is full or interval passed
        facts_count = len(self.pending_updates["facts"])
        time_passed = time.time() - self.last_sync

        return (facts_count >= self.batch_size) or (time_passed >= self.sync_interval)

    def get_pending(self):
        """Get pending updates without clearing"""
        return self.pending_updates.copy()

    def clear_pending(self):
        """Clear pending updates after successful sync"""
        self.pending_updates = {
            "facts": [],
            "emotions": [],
            "preferences": {}
        }
        self.last_sync = time.time()

    def log_sync(self, status, count):
        """Log sync operation"""
        self.sync_history.append({
            "time": time.time(),
            "status": status,
            "items": count
        })

        # Keep history small
        if len(self.sync_history) > 100:
            self.sync_history.pop(0)

    def get_stats(self):
        """Get sync statistics"""
        return {
            "pending_facts": len(self.pending_updates["facts"]),
            "pending_emotions": len(self.pending_updates["emotions"]),
            "last_sync": self.last_sync,
            "total_syncs": len(self.sync_history)
        }


# Global instance
_sync_manager = CloudSyncManager()


def get_sync_manager():
    return _sync_manager
