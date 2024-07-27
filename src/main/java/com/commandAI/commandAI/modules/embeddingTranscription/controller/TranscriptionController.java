package com.commandAI.commandAI.modules.embeddingTranscription.controller;

import com.commandAI.commandAI.modules.context.model.dto.ContextDTO;
import com.commandAI.commandAI.modules.embeddingTranscription.model.dto.TranscriptionEmbeddedDTO;
import com.commandAI.commandAI.modules.embeddingTranscription.service.IServiceTranscriptionEmbedded;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/meetings")    
@RequiredArgsConstructor
public class TranscriptionController {

    private final IServiceTranscriptionEmbedded service;

    @PostMapping("/transcriptions")
    public ResponseEntity<Void> addTranscription(@RequestBody TranscriptionEmbeddedDTO transcriptionDTO) {
        service.saveTranscription(transcriptionDTO.transcriptionText(), transcriptionDTO.embedding());
        return ResponseEntity.status(HttpStatus.CREATED).build();
    }

    @GetMapping("/transcriptions")
    public List<TranscriptionEmbeddedDTO> getAllTranscriptions() {
        return service.getAllTranscriptions();
    }

    @GetMapping("/transcriptions/{id}")
    public ResponseEntity<TranscriptionEmbeddedDTO> getTranscriptionById(@PathVariable Long id) {
        TranscriptionEmbeddedDTO transcription = service.getTranscriptionById(id);
        if (transcription == null) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND).build();
        }
        return ResponseEntity.ok(transcription);
    }

    @GetMapping("/transcriptions/similar")
    public List<TranscriptionEmbeddedDTO> findSimilarTranscriptions(@RequestParam float[] queryEmbedding) {
        return service.findSimilarTranscriptions(queryEmbedding);
    }
    @GetMapping("/last")
    public ResponseEntity<TranscriptionEmbeddedDTO> getLastTranscription() {
        TranscriptionEmbeddedDTO lastTranscription = service.getLastTranscription();
        return ResponseEntity.ok(lastTranscription);
    }
}
