package com.commandAI.commandAI.modules.context.repository;

import com.commandAI.commandAI.modules.context.model.context.Context;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface IContextRepository extends JpaRepository<Context, Long> {
    Optional<Context> findTopByOrderByCreatedAtDesc();
}
