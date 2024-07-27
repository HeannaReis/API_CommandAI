package com.commandAI.commandAI.modules.context.service.impl;

import com.commandAI.commandAI.modules.context.model.dto.ContextDTO;
import com.commandAI.commandAI.modules.context.model.context.Context;
import com.commandAI.commandAI.modules.context.repository.IContextRepository;
import com.commandAI.commandAI.modules.context.service.IContextService;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@RequiredArgsConstructor
@Service
public class ContextServiceImpl implements IContextService {

    private final IContextRepository contextRepository;

    @Override
    @Transactional
    public Context saveContext(ContextDTO data) {
        Context context = new Context();
        context.setContext(data.context());
        context = contextRepository.save(context);
        return context;
    }

    @Override
    @Transactional
    public ContextDTO getLastContext() {
        Context lastContext = contextRepository.findTopByOrderByCreatedAtDesc()
                .orElseThrow(() -> new RuntimeException("No contexts found"));
        return ContextDTO.fromEntity(lastContext);
    }
    @Override
    @Transactional
    public List<Context> findAllContext() {
        return contextRepository.findAll();
    }
}
