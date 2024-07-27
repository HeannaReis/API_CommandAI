package com.commandAI.commandAI.modules.context.model.dto;

import com.commandAI.commandAI.modules.context.model.context.Context;
import java.time.LocalDateTime;
public record ContextDTO(
        Long id,
        String context,
        LocalDateTime createdAt
) {
    public static ContextDTO fromEntity(Context context) {
        return new ContextDTO(context.getId(), context.getContext(), context.getCreatedAt());
    }
}
