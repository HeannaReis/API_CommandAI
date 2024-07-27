package com.commandAI.commandAI.modules.AIComunication.controller;

import com.commandAI.commandAI.modules.AIComunication.model.GPTCommunication;
import com.commandAI.commandAI.modules.AIComunication.model.dto.GTPCommunicationRequestDTO;
import com.commandAI.commandAI.modules.AIComunication.service.IGPTCommunicationService;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Arrays;
import java.util.List;

@RequiredArgsConstructor
@RestController
@RequestMapping("/api/question_answers")
public class GPTCommunicationController {

    private final IGPTCommunicationService service;

    @PostMapping("/save")
    public ResponseEntity<GPTCommunication> saveCommunication(@RequestBody GTPCommunicationRequestDTO dto) {
        try {
            GPTCommunication savedCommunication = service.saveCommunication(dto);
            return new ResponseEntity<>(savedCommunication, HttpStatus.CREATED);
        } catch (Exception e) {
            // Log error and return an appropriate response
            System.err.println("Erro ao salvar comunicação: " + e.getMessage());
            return new ResponseEntity<>(HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @PostMapping("/similar")
    public ResponseEntity<List<GTPCommunicationRequestDTO>> getSimilarCommunications(@RequestBody JsonNode requestBody) {
        try {
            // Validar se é um array
            if (!requestBody.isArray()) {
                throw new IllegalArgumentException("Esperado um array");
            }

            // Converter JsonNode para array de float
            float[] embedding = new ObjectMapper().convertValue(requestBody, float[].class);

            // Log para verificar o embedding recebido
            System.out.println("Embedding recebido: " + Arrays.toString(embedding));

            // Chamar o serviço com o array de float
            List<GTPCommunicationRequestDTO> similarCommunications = service.findSimilarCommunications(embedding);
            return ResponseEntity.ok(similarCommunications);
        } catch (IllegalArgumentException e) {
            System.err.println("Erro de validação: " + e.getMessage());
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(null);
        } catch (Exception e) {
            // Log error and return an appropriate response
            System.err.println("Erro ao processar a solicitação: " + e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(null);
        }
    }
}
