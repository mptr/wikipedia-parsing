from orator.migrations import Migration


class CreateTokensTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('tokens') as table:
            table.big_increments('id')
            table.drop_primary('id')
            table.integer('sentence_id')
            table.integer('pos')
            table.string('content', 1000)
            table.primary(['sentence_id', 'pos'])
            table.foreign('sentence_id').references('id').on('sentences').on_delete('cascade')

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('tokens')
