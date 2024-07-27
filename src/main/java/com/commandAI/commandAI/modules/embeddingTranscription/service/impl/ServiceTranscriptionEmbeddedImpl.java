package com.commandAI.commandAI.modules.embeddingTranscription.service.impl;

import com.commandAI.commandAI.modules.context.model.context.Context;
import com.commandAI.commandAI.modules.context.model.dto.ContextDTO;
import com.commandAI.commandAI.modules.embeddingTranscription.model.TranscriptionEmbedded;
import com.commandAI.commandAI.modules.embeddingTranscription.model.dto.TranscriptionEmbeddedDTO;
import com.commandAI.commandAI.modules.embeddingTranscription.repository.ITranscriptionEmbeddedRepository;
import com.commandAI.commandAI.modules.embeddingTranscription.service.IServiceTranscriptionEmbedded;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.stream.Collectors;

@RequiredArgsConstructor
@Service
public class ServiceTranscriptionEmbeddedImpl implements IServiceTranscriptionEmbedded {

    private final ITranscriptionEmbeddedRepository transcriptionEmbeddedRepository;

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
    public List<TranscriptionEmbeddedDTO> findSimilarTranscriptions(float[] queryEmbedding) {
        List<TranscriptionEmbedded> allTranscriptions = transcriptionEmbeddedRepository.findAll();
        return allTranscriptions.stream()
                .sorted((t1, t2) -> Double.compare(
                        cosineSimilarity(queryEmbedding, t2.getEmbedding()),
                        cosineSimilarity(queryEmbedding, t1.getEmbedding())))
                .map(transcription -> new TranscriptionEmbeddedDTO(
                        transcription.getMeetingId(),
                        transcription.getTranscriptionText(),
                        transcription.getEmbedding(),
                        transcription.getCreatedAt()))
                .collect(Collectors.toList());
    }
    @Override
    @Transactional
    public TranscriptionEmbeddedDTO getLastTranscription() {
        TranscriptionEmbedded lastTranscription = transcriptionEmbeddedRepository.findTopByOrderByCreatedAtDesc()
                .orElseThrow(() -> new RuntimeException("No contexts found"));
        return TranscriptionEmbeddedDTO.fromEntity(lastTranscription);
    }
    private double cosineSimilarity(float[] vec1, float[] vec2) {
        double dotProduct = 0.0;
        double normA = 0.0;
        double normB = 0.0;
        for (int i = 0; i < vec1.length; i++) {
            dotProduct += vec1[i] * vec2[i];
            normA += Math.pow(vec1[i], 2);
            normB += Math.pow(vec2[i], 2);
        }
        return dotProduct / (Math.sqrt(normA) * Math.sqrt(normB));
    }
}
