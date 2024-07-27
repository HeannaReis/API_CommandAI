package com.commandAI.commandAI.modules.context.controller;

import com.commandAI.commandAI.modules.context.model.dto.ContextDTO;
import com.commandAI.commandAI.modules.context.service.IContextService;
import com.commandAI.commandAI.modules.context.model.context.Context;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RequiredArgsConstructor
@RestController
@Validated
@ResponseBody
@RequestMapping("/api/contexts")
public class ContextController {

    @Autowired
    private final IContextService contextService;

    @PostMapping("/save")
    public ResponseEntity<Map<String, Object>> saveContext(@RequestBody ContextDTO data) {
        Context newContext = contextService.saveContext(data);
        Map<String, Object> response = Map.of("result", newContext);
        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }


    @GetMapping("/last")
    public ResponseEntity<ContextDTO> getLastContext() {
        ContextDTO lastContext = contextService.getLastContext();
        return ResponseEntity.ok(lastContext);
    }

    @GetMapping("/all")
    public ResponseEntity<Map<String, Object>> getAllContexts() {
        List<Context> contexts = contextService.findAllContext();
        return ResponseEntity.ok(Map.of("contexts", contexts));
    }
}
