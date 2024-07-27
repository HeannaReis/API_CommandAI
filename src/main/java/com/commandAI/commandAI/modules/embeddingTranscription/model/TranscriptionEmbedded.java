package com.commandAI.commandAI.modules.embeddingTranscription.model;

import jakarta.persistence.*;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import lombok.Data;

import java.time.LocalDateTime;

@Data
@JsonIgnoreProperties(ignoreUnknown = true)
@Entity
@Table(name = "transcriptionEmbedded")
public class TranscriptionEmbedded {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "meeting_id", nullable = false)
    private Long meetingId;

    @Column(name = "transcription_text", nullable = false, columnDefinition = "TEXT")
    private String transcriptionText;

    @Column(name = "embedding", columnDefinition = "FLOAT8[]", nullable = false)
    private float[] embedding;

    @Column(name = "created_at", nullable = false)
    private LocalDateTime createdAt;

    @PrePersist
    protected void onCreate() {
        createdAt = LocalDateTime.now();
    }

}
