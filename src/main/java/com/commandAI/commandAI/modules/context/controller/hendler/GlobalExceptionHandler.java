package com.commandAI.commandAI.modules.context.controller.hendler;

import com.commandAI.commandAI.modules.context.service.validation.ContextNotFoundException;
import lombok.Data;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.MissingServletRequestParameterException;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.context.request.WebRequest;

import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.Map;

@Data
@ControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(ContextNotFoundException.class)
    public ResponseEntity<Object> handleContextNotFoundException(ContextNotFoundException ex, WebRequest request) {
        Map<String, Object> body = new HashMap<>();
        body.put("timestamp", LocalDateTime.now());
        body.put("message", ex.getMessage());

        return new ResponseEntity<>(body, HttpStatus.NOT_FOUND);
    }
    @ExceptionHandler(MissingServletRequestParameterException.class)
    public ResponseEntity<Object> handleMissingServletRequestParameterException(MissingServletRequestParameterException ex, WebRequest request) {
        Map<String, Object> body = new HashMap<>();
        body.put("timestamp", LocalDateTime.now());
        body.put("message", "Parâmetro de requisição ausente: " + ex.getParameterName());

        return new ResponseEntity<>(body, HttpStatus.BAD_REQUEST);
    }

    // Outros handlers de exceção podem ser adicionados aqui
}