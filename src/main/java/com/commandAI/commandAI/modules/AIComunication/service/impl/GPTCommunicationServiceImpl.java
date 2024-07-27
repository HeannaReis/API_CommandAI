package com.commandAI.commandAI.modules.AIComunication.service.impl;

import com.commandAI.commandAI.modules.AIComunication.model.GPTCommunication;
import com.commandAI.commandAI.modules.AIComunication.model.dto.GTPCommunicationRequestDTO;
import com.commandAI.commandAI.modules.AIComunication.repository.IGPTCommunicationRepository;
import com.commandAI.commandAI.modules.AIComunication.service.IGPTCommunicationService;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

@RequiredArgsConstructor
@Service
public class GPTCommunicationServiceImpl implements IGPTCommunicationService {

    private final IGPTCommunicationRepository repository;

    @Override
    public GPTCommunication saveCommunication(GTPCommunicationRequestDTO dto) {
        GPTCommunication communication = new GPTCommunication();
        communication.setQuestion(dto.question());
        communication.setQuestionEmbedding(dto.questionEmbedding());
        communication.setAnswer(dto.answer());
        communication.setAnswerEmbedding(dto.answerEmbedding());
        communication.setCreatedAt(LocalDateTime.now());
        return repository.save(communication);
    }

    @Override
    public List<GTPCommunicationRequestDTO> findSimilarCommunications(float[] embedding) {
        List<GPTCommunication> allCommunications = repository.findAll();

        return allCommunications.stream()
                .filter(comm -> isSimilar(embedding, comm.getQuestionEmbedding()))
                .map(comm -> new GTPCommunicationRequestDTO(
                        comm.getQuestion(),
                        comm.getQuestionEmbedding(),
                        comm.getAnswer(),
                        comm.getAnswerEmbedding()))
                .collect(Collectors.toList());
    }

    private boolean isSimilar(float[] embedding1, float[] embedding2) {
        // Verificar se os embeddings têm o mesmo tamanho
        if (embedding1.length != embedding2.length) {
            System.err.println("Os embeddings têm tamanhos diferentes.");
            return false;
        }

        System.out.println("Embedding1: " + Arrays.toString(embedding1));
        System.out.println("Embedding2: " + Arrays.toString(embedding2));

        double dotProduct = 0.0;
        double normA = 0.0;
        double normB = 0.0;
        for (int i = 0; i < embedding1.length; i++) {
            dotProduct += embedding1[i] * embedding2[i];
            normA += Math.pow(embedding1[i], 2);
            normB += Math.pow(embedding2[i], 2);
        }
        return dotProduct / (Math.sqrt(normA) * Math.sqrt(normB)) > 0.8; // Ajuste o limiar conforme necessário
    }
}
