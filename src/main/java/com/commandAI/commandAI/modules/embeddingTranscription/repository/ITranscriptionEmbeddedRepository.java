package com.commandAI.commandAI.modules.embeddingTranscription.repository;

import com.commandAI.commandAI.modules.embeddingTranscription.model.TranscriptionEmbedded;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface ITranscriptionEmbeddedRepository extends JpaRepository<TranscriptionEmbedded, Long> {
    Optional<TranscriptionEmbedded> findTopByOrderByCreatedAtDesc();

}
