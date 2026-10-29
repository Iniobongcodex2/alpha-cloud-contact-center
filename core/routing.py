from .models import Queue, QueueMembership, AgentProfile

def get_next_agent(queue_id):
    """
    Finds the next available agent for a specific queue.
    Currently uses a simple Round Robin/Fallback logic: 
    Returns the first Available agent in the queue.
    """
    try:
        queue = Queue.objects.get(id=queue_id)
        memberships = QueueMembership.objects.filter(queue=queue, is_active=True)
        
        # Loop through agents in this queue
        for membership in memberships:
            agent = membership.agent
            # If they are Available, they get the call
            if agent.status == 'Available':
                return agent
                
        return None # No agents available
        
    except Queue.DoesNotExist:
        return None

def update_agent_status_after_call(agent, new_status='After-Call Work'):
    """
    Updates the agent's status after a call ends.
    In the future, this will trigger a timer to set them back to Available.
    """
    agent.status = new_status
    agent.save()
    return agent