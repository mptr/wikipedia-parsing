from orator.migrations import Migration


class CreateSentencesTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('sentences') as table:
            table.increments('id')
            table.integer('pos')
            table.integer('page_id')
            table.foreign('page_id').references('id').on('pages').on_delete('cascade')

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('sentences')
