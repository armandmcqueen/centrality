# VM Concepts and Lifecycle

A VM is a machine that is connected to the cluster. 

This is the lifecycle:

1. A machine is added to the cluster. It registers itself with the control plane. It chooses a name for itself. 
2. The machine sends regular heartbeats to the control plane. Machines that do this are now `live`
3. The machine stops sending a heartbeat and, after some time, is considered disconnected, but may come back. At this time, the machine is not considered `live` or `dead`. It is in `limbo`.
4. After some time without a heartbeat (or with an active death trigger), the machine is considered `dead` and not coming back

## Goal

Prevent accidentally running two machines with the same name at the same time as this will lead to confusing data.

## Invariants

- There should never be two machines with the same name at the same time. (this isn't perfectly enforced by the control plane)
- It is okay for a machine to have the same name as a previous machine as long as the previous one is `dead`
- A machine can register with the same name as a machine in limbo as long as they have identical machine specs (including hostname). This cleanly handles an agent restart.


## Cases

### A machine disconnects and then reconnects

A disconnect has a max duration. If the machine reconnects before the max duration, it is considered a reconnect.
Otherwise, it is viewed as a new machine and this case doesn't apply. If the machine is manually marked as dead,
it is considered a new machine and this case doesn't apply.

The machine can use the same name as before during registration as long as the machine specs match (which includes hostname). If the machine specs don't match, the control plane will reject the machine during registration and return an error. This should cause a complete shutdown of the agent.

TODO: This should cause an immediate error in the launch CLI

### The machine tries to use the same name as an existing machine

If they don't have matching machine specs (including hostname), the control plane will reject at registration. 
But if they do match, the control plane will accept the machine and both machines will be considered alive and 
send conflicting information.

### A machine is marked as dead and then either it reconnects or a new machine with the same name is registered

If the machine is marked as dead, the name is no longer reserved and any new machine can use it. Note that
historical machine data may be somewhat confusing in this case, as metrics are correlated by machine id.



