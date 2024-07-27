package com.commandAI.commandAI.modules.AIComunication.model.dto;

import com.fasterxml.jackson.annotation.JsonProperty;

public record GTPCommunicationRequestDTO(
        String question,
        float[] questionEmbedding,
        String answer,
        float[] answerEmbedding
) {}

