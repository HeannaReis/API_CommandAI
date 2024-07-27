package com.commandAI.commandAI.modules.AIComunication.service;

import com.commandAI.commandAI.modules.AIComunication.model.GPTCommunication;
import com.commandAI.commandAI.modules.AIComunication.model.dto.GTPCommunicationRequestDTO;

import java.util.List;

public interface IGPTCommunicationService {
    GPTCommunication saveCommunication(GTPCommunicationRequestDTO dto);
    List<GTPCommunicationRequestDTO> findSimilarCommunications(float[] embedding);
}