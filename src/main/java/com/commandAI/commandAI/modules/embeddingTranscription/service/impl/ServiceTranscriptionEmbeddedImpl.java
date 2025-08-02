package com.commandAI.commandAI.modules.embeddingTranscription.service.impl;

import com.commandAI.commandAI.modules.embeddingTranscription.model.TranscriptionEmbedded;
import com.commandAI.commandAI.modules.embeddingTranscription.model.dto.TranscriptionEmbeddedDTO;
import com.commandAI.commandAI.modules.embeddingTranscription.repository.ITranscriptionEmbeddedRepository;
import com.commandAI.commandAI.modules.embeddingTranscription.service.IServiceTranscriptionEmbedded;
import lombok.RequiredArgsConstructor;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

@RequiredArgsConstructor
@Service
public class ServiceTranscriptionEmbeddedImpl implements IServiceTranscriptionEmbedded {

    private final ITranscriptionEmbeddedRepository transcriptionEmbeddedRepository;
    private static final Logger logger = LoggerFactory.getLogger(ServiceTranscriptionEmbeddedImpl.class);

    @Override
    @Transactional
    public void saveTranscription(String transcriptionText, float[] embedding) {
        TranscriptionEmbedded transcription = new TranscriptionEmbedded();
        transcription.setTranscriptionText(transcriptionText);
        transcription.setEmbedding(embedding);
        System.out.println(transcription);
        transcriptionEmbeddedRepository.save(transcription);
    }

    @Override
    @Transactional
    public List<TranscriptionEmbeddedDTO> getAllTranscriptions() {
        return transcriptionEmbeddedRepository.findAll().stream()
                .map(transcription -> new TranscriptionEmbeddedDTO(
                        transcription.getMeetingId(),
                        transcription.getTranscriptionText(),
                        transcription.getEmbedding(),
                        transcription.getCreatedAt()))
                .collect(Collectors.toList());
    }

    @Override
    @Transactional
    public TranscriptionEmbeddedDTO getTranscriptionById(Long id) {
        TranscriptionEmbedded transcription = transcriptionEmbeddedRepository.findById(id).orElse(null);
        if (transcription == null) {
            return null;
        }
        return new TranscriptionEmbeddedDTO(
                transcription.getMeetingId(),
                transcription.getTranscriptionText(),
                transcription.getEmbedding(),
                transcription.getCreatedAt());
    }

    @Override
    @Transactional
    public TranscriptionEmbeddedDTO getLastTranscription() {
        TranscriptionEmbedded lastTranscription = transcriptionEmbeddedRepository.findTopByOrderByCreatedAtDesc()
                .orElseThrow(() -> new RuntimeException("No contexts found"));
        return TranscriptionEmbeddedDTO.fromEntity(lastTranscription);
    }
}