package com.commandAI.commandAI.modules.AIComunication.model;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import jakarta.persistence.*;
import lombok.Data;

import java.time.LocalDateTime;
@Data
@Entity
@JsonIgnoreProperties(ignoreUnknown = true)
@Table(name = "gpt_communication")
public class GPTCommunication {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "question", nullable = false, columnDefinition = "TEXT")
    private String question;

    @Column(name = "answer", nullable = false, columnDefinition = "TEXT")
    private String answer;

    @Column(name = "question_embedding", columnDefinition = "FLOAT8[]", nullable = false)
    private float[] questionEmbedding;

    @Column(name = "answer_embedding", columnDefinition = "FLOAT8[]", nullable = false)
    private float[] answerEmbedding;

    @Column(name = "created_at", nullable = false)
    private LocalDateTime createdAt;

}