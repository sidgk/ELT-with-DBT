Welcome to your new dbt project!

### Using the starter project

Try running the following commands:
<!-- Builds the entire project, run models, test tests snapshot snapshots and seed seeds. -->
- dbt build 
<!-- Test all the tests defined for the tag source. -->
- dbt test --select tag:source 
<!-- This command will build upstream and the downstream models -->
- dbt build --select +dim_transactions+
<!-- Buiilds all the models which are tagged with payments tag. -->
- dbt build --select tag:payments


### Resources:
- Learn more about dbt [in the docs](https://docs.getdbt.com/docs/introduction)
- Check out [Discourse](https://discourse.getdbt.com/) for commonly asked questions and answers
- Join the [dbt community](http://community.getbdt.com/) to learn from other analytics engineers
- Find [dbt events](https://events.getdbt.com) near you
- Check out [the blog](https://blog.getdbt.com/) for the latest news on dbt's development and best practices
