package com.commandAI.commandAI.modules.embeddingTranscription.model.dto;

import com.commandAI.commandAI.modules.context.model.context.Context;
import com.commandAI.commandAI.modules.context.model.dto.ContextDTO;
import com.commandAI.commandAI.modules.embeddingTranscription.model.TranscriptionEmbedded;

import java.time.LocalDateTime;

public record TranscriptionEmbeddedDTO(
        Long meetingId,
        String transcriptionText,
        float[] embedding,
        LocalDateTime createdAt
) {
    public static TranscriptionEmbeddedDTO fromEntity(TranscriptionEmbedded transcriptionEmbedded) {
        return new TranscriptionEmbeddedDTO(transcriptionEmbedded.getMeetingId(), transcriptionEmbedded.getTranscriptionText(), transcriptionEmbedded.getEmbedding(), transcriptionEmbedded.getCreatedAt());
    }
}
