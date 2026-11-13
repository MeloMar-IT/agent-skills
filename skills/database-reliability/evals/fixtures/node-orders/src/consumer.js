// Kafka consumer for the order service (kafkajs-style API).
export async function run(consumer, handler) {
  await consumer.run({
    autoCommit: true,
    eachMessage: async ({ message }) => {
      await handler(message);
    },
  });
}
