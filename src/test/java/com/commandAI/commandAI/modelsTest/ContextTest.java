package com.commandAI.commandAI.modelsTest;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import com.commandAI.commandAI.modules.context.model.context.Context;
import java.time.LocalDateTime;

import static org.junit.jupiter.api.Assertions.*;

public class ContextTest {

    private Context context;

    @BeforeEach
    public void setUp() {
        context = new Context();
    }

    @Test
    public void testSetAndGetId() {
        Long id = 1L;
        context.setId(id);
        assertEquals(id, context.getId());
    }

    @Test
    public void testSetAndGetContext() {
        String testContext = "Sample context";
        context.setContext(testContext);
        assertEquals(testContext, context.getContext());
    }

    @Test
    public void testSetAndGetCreatedAt() {
        LocalDateTime now = LocalDateTime.now();
        context.setCreatedAt(now);
        assertEquals(now, context.getCreatedAt());
    }
}
