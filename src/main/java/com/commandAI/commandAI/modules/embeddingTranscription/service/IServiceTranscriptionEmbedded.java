package com.commandAI.commandAI.modules.embeddingTranscription.service;

import com.commandAI.commandAI.modules.context.model.dto.ContextDTO;
import com.commandAI.commandAI.modules.embeddingTranscription.model.dto.TranscriptionEmbeddedDTO;

import java.util.List;

public interface IServiceTranscriptionEmbedded {
    void saveTranscription(String transcriptionText, float[] embedding);
    List<TranscriptionEmbeddedDTO> getAllTranscriptions();
    TranscriptionEmbeddedDTO getTranscriptionById(Long id);
    List<TranscriptionEmbeddedDTO> findSimilarTranscriptions(float[] queryEmbedding);
    TranscriptionEmbeddedDTO getLastTranscription();
}
