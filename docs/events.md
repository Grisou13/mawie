Most of the components in the app use events. All the components that trigger events extend the class *Eventable* .

# Events basics

Events are objects allowing compoenents (any compoenent) to talk to each other.

Events have timeouts, by default they don't (event.timeout == §), this means that it will be able to cycle only once in the app before getting destroyed.

