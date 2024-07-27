package com.commandAI.commandAI.modules.AIComunication.repository;

import com.commandAI.commandAI.modules.AIComunication.model.GPTCommunication;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface IGPTCommunicationRepository extends JpaRepository<GPTCommunication, Long> {

}