package com.commandAI.commandAI.modules.context.service;

import com.commandAI.commandAI.modules.context.model.context.Context;
import com.commandAI.commandAI.modules.context.model.dto.ContextDTO;

import java.util.List;

public interface IContextService {
    Context saveContext(ContextDTO data);
    ContextDTO getLastContext();
    List<Context> findAllContext();
}
