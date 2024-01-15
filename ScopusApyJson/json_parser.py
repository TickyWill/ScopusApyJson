__all__ = ['parse_json_data_to_scopus_df',]

    
def _built_date(dic, key):
    # Standard library imports
    import calendar
    
    # Local library imports
    from ScopusApyJson.json_utils import check_true_to_append
    from ScopusApyJson.json_utils import get_json_key_value
        
    dateitems = get_json_key_value(dic, key)
    dateitems_list = []  
    dateitems_list = check_true_to_append(dateitems, '@day', dateitems_list)
    item_num  = 0
    dateitems_list = check_true_to_append(dateitems, '@month', dateitems_list)
    item_num += 1
    month_num = int(dateitems_list[item_num])
    dateitems_list[item_num] = calendar.month_name[month_num]
    dateitems_list = check_true_to_append(dateitems, '@year', dateitems_list)
    date = " ".join(dateitems_list)
    
    return date


def _parse_source_info(json_data, article_dic):
    '''Parse the field "source" under the top 
    "field asbtracts-retrieval-response/item/bibrecord/head".
    '''
    
    # Local library imports
    from ScopusApyJson.json_utils import check_not_none
    from ScopusApyJson.json_utils import check_true_to_append
    from ScopusApyJson.json_utils import check_true_to_set
    from ScopusApyJson.json_utils import get_json_key_value
    
    source_dict                             = get_json_key_value(json_data, "source")
    article_dic['Year']                     = get_json_key_value(source_dict, "year")
    article_dic['Source title']             = get_json_key_value(source_dict, 'sourcetitle')
    article_dic['Abbreviated Source Title'] = get_json_key_value(source_dict, 'sourcetitle-abbrev')
    article_dic['CODEN']                    = get_json_key_value(source_dict, 'codencode')
    
    # Parsing issn
    issn_info = get_json_key_value(source_dict, 'issn')
    if check_not_none(issn_info):
        if not isinstance(issn_info, list):
            article_dic['ISSN'] = get_json_key_value(issn_info, '$')
        else:    
            for issn_dict in issn_info:
                issn_type = get_json_key_value(issn_dict, '@type')
                if issn_type == "print": article_dic['ISSN'] = get_json_key_value(issn_dict, '$')

    #Parsing isbn if available  
    isbn_info = get_json_key_value(source_dict, 'isbn')
    if check_not_none(isbn_info):
        if not isinstance(isbn_info, list):
            article_dic['ISBN'] = get_json_key_value(isbn_info, '$')            
        else:
            for isbn_dict in isbn_info:
                isbn_type = get_json_key_value(isbn_dict, '@type')
                if isbn_type == "print": article_dic['ISBN'] = get_json_key_value(isbn_dict, '$')
                
    # Parsing conference info if available
    conference_info = get_json_key_value(source_dict, 'additional-srcinfo')
    if check_not_none(conference_info):
        conferenceinfo = get_json_key_value(conference_info, 'conferenceinfo')
        if check_not_none(conferenceinfo):
            confevent = get_json_key_value(conferenceinfo, 'confevent')
            if check_not_none(confevent):
                article_dic['Conference name'] = get_json_key_value(confevent, 'confname')                
                article_dic['Conference code'] = get_json_key_value(confevent, 'confcode')
                conflocation = get_json_key_value(confevent, 'conflocation')
                if check_not_none(conflocation): 
                    article_dic['Conference location'] = get_json_key_value(conflocation, 'city')
                confdates = get_json_key_value(confevent, 'confdate')
                if check_not_none(confdates):
                    start_date = _built_date(confdates, 'startdate')
                    end_date   = _built_date(confdates, 'enddate')                   
                    article_dic['Conference date'] = start_date + " through " + end_date        
    
    # Parsing volisspag if available          
    article_dic = check_true_to_set(source_dict, 'article-number', article_dic, 'Art. No.')
    volisspag   = get_json_key_value(source_dict, "volisspag")
    if check_not_none(volisspag):
        voliss      = get_json_key_value(volisspag, "voliss")
        article_dic = check_true_to_set(voliss, '@volume', article_dic, 'Volume')
        article_dic = check_true_to_set(voliss, '@issue', article_dic, 'Issue')
        pagerange   = get_json_key_value(volisspag, "pagerange")
        if check_not_none(pagerange): 
            article_dic['Page start'] = get_json_key_value(pagerange, '@first')
            article_dic['Page end']   = get_json_key_value(pagerange, '@last')
            article_dic['Page count'] = str(int(article_dic['Page end']) - int(article_dic['Page start']))
    
    # Parsing publication stage
    stage_info  = get_json_key_value(source_dict, 'publicationdate')
    if "month" in stage_info.keys(): 
        article_dic['Publication Stage'] = "Final" 
    else:
        article_dic['Publication Stage'] = "Article in press"

        
def _parse_citation_info(json_data, article_dic):
    '''Parse the field "citation-info" under the top field 
    "asbtracts-retrieval-response/item/bibrecord/head".
    '''
    # Local library imports
    from ScopusApyJson.json_utils import check_not_none
    from ScopusApyJson.json_utils import get_json_key_value
    
    citation_info = get_json_key_value(json_data, 'citation-info')
    language_dict = get_json_key_value(citation_info, 'citation-language')
    if check_not_none(language_dict): 
        article_dic['Language of Original Document'] = get_json_key_value(language_dict, '@language')

    
def _parse_ordered_authors(json_data, article_dic):
    '''Parse the field "author" under the top field 
    "astracts-retrieval-response/authors".
    The field "author" is a dict if there is only 
    one author otherwise it is a list of dict.
    '''
    
    # Local library imports
    from ScopusApyJson.json_utils import get_json_key_value
    
    authors            = []
    authors_ids        = []
    authors_full_names = []
    
    auths_field = get_json_key_value(json_data, "authors")
    auths_group = get_json_key_value(auths_field, "author")
    if not isinstance(auths_group, list) : auths_group = [auths_group]
        
    for auths in auths_group:
        auth_id             = get_json_key_value(auths, '@auid')
        auth_preferred_name = get_json_key_value(auths, 'preferred-name')
        auth_name           = get_json_key_value(auth_preferred_name, 'ce:indexed-name')
        auth_surname        = get_json_key_value(auth_preferred_name, 'ce:surname')
        auth_given_name     = get_json_key_value(auth_preferred_name, 'ce:given-name')
                
        authors.append(auth_name)
        authors_ids.append(auth_id)
        authors_full_names.append(f'{auth_surname}, {auth_given_name} ({auth_id})')

    article_dic['Authors']           = '; '.join(authors)
    article_dic['Author(s) ID']      = '; '.join(authors_ids)
    article_dic['Author full names'] = '; '.join(authors_full_names)
    
    
def _parse_authors_affiliations(json_data, article_dic):
    '''Parse the field "author-group" under the top field 
    "abstracts-retrieval-response/item/bibrecord/head".
    The field "author-group" is a dict if there is only one author, 
    otherwise it is a list of dict .
    '''
    
    # Standard library imports
    from collections import defaultdict
    
    # Local library imports
    from ScopusApyJson.json_utils import check_true_to_append
    from ScopusApyJson.json_utils import get_json_key_value
    
    authors_with_affiliations_dict = defaultdict(list)
    authors_with_affiliations_list = []
    affiliations_list              = []
    ordered_authors                = article_dic['Authors'].split('; ')
    
    affiliations_group = get_json_key_value(json_data, 'author-group')
    if not isinstance(affiliations_group, list) : affiliations_group = [affiliations_group]
        
    for affiliation_dict in affiliations_group:
        affiliation = get_json_key_value(affiliation_dict, 'affiliation')
    
        # Building affiliation full address
        organizations_list = get_json_key_value(affiliation, 'organization')
        if not isinstance(organizations_list, list) : organizations_list = [organizations_list]
        address_items_list = []
        for organization_dict in organizations_list:
            address_items_list.append(get_json_key_value(organization_dict, '$'))        
        address_items_list = check_true_to_append(affiliation, 'address-part', address_items_list)
        address_items_list = check_true_to_append(affiliation, 'city', address_items_list)
        address_items_list = check_true_to_append(affiliation, 'postal-code', address_items_list)
        address_items_list = check_true_to_append(affiliation, 'country', address_items_list)
        affiliation_address = ', '.join(address_items_list)
      
        # Appending "affiliation_address" to "affiliations_list"
        affiliations_list.append(affiliation_address)
        
        # Appending "affiliation_address" to "authors_with_affiliations_dict" for each author of the "affiliation_authors_list"
        affiliation_authors_list = get_json_key_value(affiliation_dict, 'author')
        if not isinstance(affiliation_authors_list, list) : affiliation_authors_list = [affiliation_authors_list]
        for author in affiliation_authors_list:
            author_preferred_name = get_json_key_value(author, 'preferred-name')
            author_name           = get_json_key_value(author_preferred_name, 'ce:indexed-name')
            authors_with_affiliations_dict[author_name].append(affiliation_address)
            
    # Ordering the "authors_with_affiliations_list" in the order of the "ordered_authors"
    for author in ordered_authors:
        author_affiliations_list = authors_with_affiliations_dict[author]
        authors_with_affiliations_list.append(f"{author}, {', '.join(author_affiliations_list)}")        

    article_dic['Authors with affiliations'] = '; '.join(authors_with_affiliations_list)
    article_dic['Affiliations']              = '; '.join(affiliations_list)

    
def _parse_correspondence_address(json_data, article_dic):
    '''Parse the field "correspondence" under the top field 
    "abstracts-retrieval-response/item/bibrecord/head".
    The field "correspondence" is a dict if there is only one corresponding person, 
    otherwise it is a list of dict.
    '''
    # Local library imports
    from ScopusApyJson.json_utils import check_true_to_append
    from ScopusApyJson.json_utils import get_json_key_value    
    
    person_address_list = []
    
    correspondence_list = get_json_key_value(json_data, 'correspondence')   
    if not isinstance(correspondence_list, list) : correspondence_list = [correspondence_list]
    for correspondence_dict in correspondence_list:        
        correspondence_person_dict = get_json_key_value(correspondence_dict, 'person')
        correspondence_person      = get_json_key_value(correspondence_person_dict, 'ce:indexed-name')
               
        # Building affiliation full address
        affiliation = get_json_key_value(correspondence_dict, 'affiliation')
        organizations_list = get_json_key_value(affiliation, 'organization')
        if not isinstance(organizations_list, list) : organizations_list = [organizations_list]
        address_items_list = []
        for organization_dict in organizations_list:
            address_items_list.append(get_json_key_value(organization_dict, '$'))
        address_items_list = check_true_to_append(affiliation, 'address-part', address_items_list)
        address_items_list = check_true_to_append(affiliation, 'city', address_items_list)
        address_items_list = check_true_to_append(affiliation, 'postal-code', address_items_list)
        address_items_list = check_true_to_append(affiliation, 'country', address_items_list)
        correspondence_address = ', '.join(address_items_list)
        
        person_address_list.append(correspondence_person + "; " + correspondence_address)
        
    article_dic['Correspondence Address'] = '; '.join(person_address_list)

    
def _parse_references(json_data, article_dic):
    '''Parse the field "bibliography" under the top field 
    "abstracts-retrieval-response/item/bibrecord/tail".
    The field "bibliography" is a dict keyyed by "$" if it is not None.
    '''
    # Local library imports
    from ScopusApyJson.json_utils import check_not_none
    from ScopusApyJson.json_utils import get_json_key_value
    
    ref_text_list = []
    tail             = get_json_key_value(json_data, 'tail')
    bibliography     = get_json_key_value(tail, 'bibliography')
    references_list  = get_json_key_value(bibliography, 'reference')
    if not isinstance(references_list, list): references_list = [references_list]

    for ref_dict in references_list:
        ref_item_list = []
        
        ref_info    = get_json_key_value(ref_dict, 'ref-info')
        ref_authors = get_json_key_value(ref_info, 'ref-authors')
        author_dict = get_json_key_value(ref_authors, 'author')
        et_al       = ""
        if isinstance(author_dict, list): 
            author_dict = author_dict[0]
            et_al       = " et al."
        author_name = get_json_key_value(author_dict, 'ce:indexed-name')
        if check_not_none(author_name):
            authors     = author_name + et_al                
            ref_item_list.append(authors)

        ref_title = get_json_key_value(ref_info, 'ref-title')
        title     = get_json_key_value(ref_title, 'ref-titletext')
        if check_not_none(title): ref_item_list.append(title)

        source = get_json_key_value(ref_info, 'ref-sourcetitle')
        if check_not_none(source): ref_item_list.append(source)

        ref_volisspag = get_json_key_value(ref_info, 'ref-volisspag')
        voliss        = get_json_key_value(ref_volisspag, 'voliss')
        volume        = get_json_key_value(voliss, '@volume')
        issue         = get_json_key_value(voliss, '@issue')
        pagerange     = get_json_key_value(ref_volisspag, 'pagerange')
        page_first    = get_json_key_value(pagerange, '@first')
        page_last     = get_json_key_value(pagerange, '@last')
        if check_not_none(volume): ref_item_list.append(volume)        
        if check_not_none(issue): ref_item_list.append(issue)
        if check_not_none(page_first) and check_not_none(page_last): 
            ref_item_list.append('pp. ' + page_first + '-' + page_last)

        ref_publicationyear = get_json_key_value(ref_info, 'ref-publicationyear')
        year                = get_json_key_value(ref_publicationyear, '@first')
        if check_not_none(year): ref_item_list.append("(" + year + ")")

        refd_itemidlist = get_json_key_value(ref_info, 'refd-itemidlist')
        itemid_list     = get_json_key_value(refd_itemidlist, 'itemid')
        if not isinstance(itemid_list, list): itemid_list = [itemid_list]
        doi = None
        for itemid_dict in itemid_list:
            itemid_type = get_json_key_value(itemid_dict, '@idtype')            
            if itemid_type == "DOI": doi = get_json_key_value(itemid_dict, '$')
        if check_not_none(doi): ref_item_list.append(doi)
        
        ref_text = get_json_key_value(ref_info, 'ref-text')
        if check_not_none(ref_text): ref_item_list.append(ref_text)

        full_ref = ', '.join(ref_item_list)
        ref_text_list.append(full_ref)
    article_dic['References'] = '; '.join(ref_text_list)            

        
def _parse_index_keywords(json_data, article_dic):
    '''Parse the field "idxterms" under the top field "abstracts-retrieval-response".
    The field "idxterms" is a dict keyyed by "$" if it is not None.
    '''
    # Local library imports
    from ScopusApyJson.json_utils import check_not_none
    from ScopusApyJson.json_utils import get_json_key_value
    
    idxterms = get_json_key_value(json_data, 'idxterms')
    if check_not_none(idxterms):
        idxterms_list = get_json_key_value(idxterms, 'mainterm')
        if not isinstance(idxterms_list, list): idxterms_list = [idxterms_list]
        article_dic['Index Keywords'] = '; '.join([x['$'] for x in idxterms_list])

        
def _parse_author_keywords(json_data, article_dic):
    '''Parse the field "authkeywords" under the top field "abstracts-retrieval-response".
    The field "authkeywords" is a dict keyyed by "$" if it is not None.
    '''
    # Local library imports
    from ScopusApyJson.json_utils import check_not_none
    from ScopusApyJson.json_utils import get_json_key_value
    
    author_keywords = get_json_key_value(json_data, 'authkeywords')
    if check_not_none(author_keywords):
        author_keywords_list = get_json_key_value(author_keywords, 'author-keyword')
        if check_not_none(author_keywords_list):
            if not isinstance(author_keywords_list, list): author_keywords_list = [author_keywords_list]
            article_dic['Author Keywords'] = '; '.join([x['$'] for x in author_keywords_list])   


def _parse_coredata(json_data, article_dic):
    '''Parse the field "coredata" under the top field "abstracts-retrieval-response".
    '''
    # Local library imports
    from ScopusApyJson.json_utils import get_json_key_value
    
    coredata_dict                = get_json_key_value(json_data, 'coredata')
    article_dic['Title']         = get_json_key_value(coredata_dict, 'dc:title')
    article_dic['DOI']           = get_json_key_value(coredata_dict, 'prism:doi')
    article_dic['EID']           = get_json_key_value(coredata_dict, 'eid')
    article_dic['Document Type'] = get_json_key_value(coredata_dict, 'subtypeDescription')
    article_dic['PubMed ID']     = get_json_key_value(coredata_dict, 'pubmed-id')
    article_dic['Publisher']     = get_json_key_value(coredata_dict, 'dc:publisher')
    article_dic['Cited by']      = get_json_key_value(coredata_dict, 'citedby-count')
    article_dic['Abstract']      = get_json_key_value(coredata_dict, 'dc:description')
    
    # Parsing open access
    openaccess = get_json_key_value(coredata_dict, 'openaccess')
    if openaccess == "2" : 
        article_dic['Open Access'] = "All Open Access; Green Open Access"
    if openaccess == "1" : 
        article_dic['Open Access'] = "All Open Access; Green Open Access; Gold Open Access (Hybrid?)"
    
    # Parsing link
    link_info = get_json_key_value(coredata_dict, 'link')
    if isinstance(link_info, list):        
        for link_dict in link_info:
            link_rel = get_json_key_value(link_dict, '@rel')
            if link_rel == "scopus": article_dic['Link'] = get_json_key_value(link_dict, '@href')
    else:
        link_dict =  link_info
        article_dic['Link'] = get_json_key_value(link_dict, '@href')
    

def _make_json_data_dict(json_data, article_dic):
    
    # Setting default values (not in json_data)
    article_dic['Source'] = "Scopus"
    
    # Parsing json data
    _parse_ordered_authors(json_data, article_dic)
    _parse_authors_affiliations(json_data, article_dic)
    _parse_correspondence_address(json_data, article_dic)
    _parse_source_info(json_data, article_dic)
    _parse_citation_info(json_data, article_dic)    
    _parse_references(json_data, article_dic)
    _parse_index_keywords(json_data, article_dic)
    _parse_author_keywords(json_data, article_dic)
    _parse_coredata(json_data, article_dic)
    
    return article_dic


def parse_json_data_to_scopus_df(json_data):
    '''The function `parse_json_data_to_scopus_df` parses 
    the hierarchical dict of the data "json_data". Then it builds
    the dataframe which colums are specified by the global 
    "SELECTED_SCOPUS_COLUMNS_NAMES".
    
    Args:
        json_data (dict): The hierarchical dict built by the function 
        `get_doi_json_data_from_api`.
        
    Returns:
        (pandas.core.frame.DataFrame): The dataframe resulting 
        from the hierarchical dict parsing.
    '''
    # Standard library imports
    import json as json
    
    # 3rd party imports
    import pandas as pd
    
    # Globals imports 
    from ScopusApyJson.GLOBALS import PARSED_SCOPUS_COLUMNS_NAMES
    from ScopusApyJson.GLOBALS import SELECTED_SCOPUS_COLUMNS_NAMES
    
    article_dic = {}
    for key in set(PARSED_SCOPUS_COLUMNS_NAMES):
        article_dic[key] = None 

    article_dic = _make_json_data_dict(json_data, article_dic)               
    
    scopus_df = pd.DataFrame.from_dict([article_dic])
    scopus_df = scopus_df[SELECTED_SCOPUS_COLUMNS_NAMES]
    
    return scopus_df
