package com.commandAI.commandAI.modules.embeddingTranscription.service;

import com.commandAI.commandAI.modules.embeddingTranscription.model.dto.TranscriptionEmbeddedDTO;

import java.util.List;

public interface IServiceTranscriptionEmbedded {
    void saveTranscription(String transcriptionText, float[] embedding);

    List<TranscriptionEmbeddedDTO> getAllTranscriptions();

    TranscriptionEmbeddedDTO getTranscriptionById(Long id);

    TranscriptionEmbeddedDTO getLastTranscription();
}