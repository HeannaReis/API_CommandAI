package com.commandAI.commandAI.modules.context.service.validation;

public class ContextNotFoundException extends RuntimeException {
    public ContextNotFoundException(String message) {
        super(message);
    }
}
