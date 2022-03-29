from datetime import date, datetime
from typing import Set, List, Dict
import os
from utils import IssuePackage, REQUEST_REPO, AUTO_ASSIGN_LABEL, AUTO_PARSE_LABEL, get_origin_link_and_tag,\
    MULTI_LINK_LABEL
import re
import logging
import time
from random import randint
from github import Github
from github.Repository import Repository

_LOG = logging.getLogger(__name__)

# assignee dict which will be assigned to handle issues
_LANGUAGE_OWNER = {'msyyc'}

# 'github assignee': 'token'
_ASSIGNEE_TOKEN = {'msyyc': os.getenv('AZURESDK_BOT_TOKEN')}

_SWAGGER_URL = 'https://github.com/Azure/azure-rest-api-specs/blob/main/specification'
_SWAGGER_PULL = 'https://github.com/Azure/azure-rest-api-specs/pull'


class IssueProcess:
    """
    # won't be changed anymore after __init__
    request_repo_dict = {}  # request repo instance generated by different token
    owner = ''  # issue owner
    assignee_candidates = {}  # assignee candidates who will be assigned to handle issue
    language_owner = {}  # language owner who may handle issue

    # will be changed by order
    issue_package = None  # issue that needs to handle
    assignee = ''
    bot_advice = []  # bot advice to help SDK owner
    target_readme_tag = ''  # swagger content that customers want
    readme_link = ''  # https link which swagger definition is in
    default_readme_tag = ''  # configured in `README.md`
    package_name = ''  # target package name
    target_date = ''  # target release date asked by customer
    date_from_target = 0
    """

    def __init__(self, issue_package: IssuePackage, request_repo_dict: Dict[str, Repository],
                 assignee_candidates: Set[str], language_owner: Set[str]):
        self.issue_package = issue_package
        self.request_repo_dict = request_repo_dict
        self.assignee = issue_package.issue.assignee.login if issue_package.issue.assignee else ''
        self.owner = issue_package.issue.user.login
        self.assignee_candidates = assignee_candidates
        self.language_owner = language_owner
        self.bot_advice = []
        self.target_readme_tag = ''
        self.readme_link = ''
        self.default_readme_tag = ''
        self.package_name = ''
        self.target_date = ''
        self.date_from_target = 0

    def get_issue_body(self) -> List[str]:
        return [i for i in self.issue_package.issue.body.split("\n") if i]

    def handle_link_contains_commit(self, link: str) -> str:
        if 'commit' in link:
            commit_sha = link.split('commit/')[-1]
            commit = self.issue_package.rest_repo.get_commit(commit_sha)
            link = commit.files[0].blob_url
            link = re.sub('blob/(.*?)/specification', 'blob/main/specification', link)
        return link

    def comment(self, message: str) -> None:
        self.issue_package.issue.create_comment(message)

    def get_readme_from_pr_link(self, link: str) -> str:
        pr_number = int(link.replace(f"{_SWAGGER_PULL}/", "").strip('/'))

        # Get Readme link
        pr_info = self.issue_package.rest_repo.get_pull(number=pr_number)
        pk_url_name = set()
        for pr_changed_file in pr_info.get_files():
            contents_url = pr_changed_file.contents_url
            if '/resource-manager' not in contents_url:
                continue
            try:
                pk_url_name.add(re.findall(r'/specification/(.*?)/resource-manager/', contents_url)[0])
            except Exception as e:
                continue
        readme_link = [f'{_SWAGGER_URL}/{item}/resource-manager' for item in pk_url_name]
        if len(readme_link) > 1:
            multi_link = ', '.join(readme_link)
            pr = f"{_SWAGGER_PULL}/{pr_number}"
            self.comment(
                f'Hi, @{self.assignee}, by parsing {pr}, there are multi service link: {multi_link}. Please decide which one is the right.')
            self.add_label(MULTI_LINK_LABEL)
            raise Exception(f'multi link in "{pr}"')

        return readme_link[0]

    def get_readme_link(self, origin_link: str):
        # check whether link is valid
        if 'azure-rest-api-specs' not in origin_link:
            self.comment(f'Hi, @{self.owner}, "{origin_link}" is not valid link. Please follow [doc]'
                         f'(https://github.com/Azure/azure-rest-api-specs/blob/main/documentation/release-request/'
                         f'rules-for-release-request.md#2-link-to-pr-or-spec-if-pr-unavailable) to provide valid link like '
                         f'"https://github.com/Azure/azure-rest-api-specs/pull/16750" or '
                         f'"https://github.com/Azure/azure-rest-api-specs/tree/main/'
                         f'specification/network/resource-manager"')
            raise Exception('Invalid link!')
        elif 'azure-rest-api-specs-pr' in origin_link:
            self.comment(f'Hi @{self.owner}, only [Azure/azure-rest-api-specs](https://github.com/Azure/'
                         f'azure-rest-api-specs) is permitted to publish SDK, [Azure/azure-rest-api-specs-pr]'
                         f'(https://github.com/Azure/azure-rest-api-specs-pr) is not permitted. '
                         f'Please paste valid link!')
            raise Exception('Invalid link from private repo')

        # change commit link to pull json link(i.e. https://github.com/Azure/azure-rest-api-specs/
        # commit/77f5d3b5d2#diff-708c2fb)
        link = self.handle_link_contains_commit(origin_link)

        # if link is a pr, it can get both pakeage name and readme link.
        if 'pull' in link:
            self.readme_link = self.get_readme_from_pr_link(link)
        # if link is a url(i.e. https://github.com/Azure/azure-rest-api-specs/blob/main/specification/
        # xxx/resource-manager/readme.md)
        elif '/resource-manager' not in link:
            # (i.e. https://github.com/Azure/azure-rest-api-specs/tree/main/specification/xxxx)
            self.readme_link = link + '/resource-manager'
        else:
            self.readme_link = link.split('/resource-manager')[0] + '/resource-manager'

    def get_default_readme_tag(self) -> None:
        pattern_resource_manager = re.compile(r'/specification/([\w-]+/)+resource-manager')
        readme_path = pattern_resource_manager.search(self.readme_link).group() + '/readme.md'
        contents = str(self.issue_package.rest_repo.get_contents(readme_path).decoded_content)
        pattern_tag = re.compile(r'tag: package-[\w+-.]+')
        self.default_readme_tag = pattern_tag.search(contents).group().split(':')[-1].strip()

    def edit_issue_body(self) -> None:
        issue_body_list = [i for i in self.issue_package.issue.body.split("\n") if i]
        issue_body_list.insert(0, f'\n{self.readme_link.replace("/readme.md", "")}')
        issue_body_up = ''
        # solve format problems
        for raw in issue_body_list:
            if raw == '---\r' or raw == '---':
                issue_body_up += '\n'
            issue_body_up += raw + '\n'
        self.issue_package.issue.edit(body=issue_body_up)

    def check_tag_consistency(self) -> None:
        if self.default_readme_tag != self.target_readme_tag:
            self.comment(f'Hi, @{self.owner}, according to [rule](https://github.com/Azure/azure-rest-api-specs/blob/'
                         f'main/documentation/release-request/rules-for-release-request.md#3-readme-tag-to-be-released),'
                         f' your **Readme Tag** is `{self.target_readme_tag}`, but in [readme.md]({self.readme_link}#basic-information) '
                         f'it is still `{self.default_readme_tag}`, please modify the readme.md or your '
                         f'**Readme Tag** above ')

    def auto_parse(self) -> None:
        if AUTO_PARSE_LABEL in self.issue_package.labels_name:
            return

        self.add_label(AUTO_PARSE_LABEL)
        issue_body_list = self.get_issue_body()

        # Get the origin link and readme tag in issue body
        origin_link, self.target_readme_tag = get_origin_link_and_tag(issue_body_list)

        # get readme_link
        self.get_readme_link(origin_link)

        # get default tag with readme_link
        self.get_default_readme_tag()

        self.check_tag_consistency()

        self.edit_issue_body()

    def add_label(self, label: str) -> None:
        self.issue_package.issue.add_to_labels(label)
        self.issue_package.labels_name.add(label)

    def update_assignee(self, assignee_to_del: str, assignee_to_add: str) -> None:
        if assignee_to_del:
            self.issue_package.issue.remove_from_assignees(assignee_to_del)
        self.issue_package.issue.add_to_assignees(assignee_to_add)
        self.assignee = assignee_to_add

    def log(self, message: str) -> None:
        _LOG.info(f'issue {self.issue_package.issue.number}: {message}')

    def request_repo(self) -> Repository:
        return self.request_repo_dict[self.assignee]

    def update_issue_instance(self) -> None:
        self.issue_package.issue = self.request_repo().get_issue(self.issue_package.issue.number)

    def auto_assign(self) -> None:
        if AUTO_ASSIGN_LABEL in self.issue_package.labels_name:
            self.update_issue_instance()
            return
        # assign averagely
        assignees = list(self.assignee_candidates)
        random_idx = randint(0, len(assignees) - 1) if len(assignees) > 1 else 0
        assignee = assignees[random_idx]

        # update assignee
        if self.assignee != assignee:
            self.log(f'remove assignee "{self.issue_package.issue.assignee}" and add "{assignee}"')
            self.assignee = assignee
            self.update_issue_instance()
            self.update_assignee(self.issue_package.issue.assignee, assignee)
        else:
            self.update_issue_instance()
        self.add_label(AUTO_ASSIGN_LABEL)

    def new_issue_policy(self):
        new_issue_advice = 'new issue.'
        if self.issue_package.issue.comments == 0:
            self.bot_advice.append(new_issue_advice)
        else:
            # issue that no comment from language owner will also be treated as new issue
            comment_from_owner = set(comment.user.login for comment in self.issue_package.issue.get_comments()
                                     if comment.user.login in self.language_owner)
            if not comment_from_owner:
                self.bot_advice.append(new_issue_advice)

    def new_comment_policy(self):
        if self.issue_package.issue.comments == 0:
            return
        comments = [(comment.updated_at.timestamp(), comment.user.login) for comment in
                    self.issue_package.issue.get_comments()]
        comments.sort()
        latest_comments = comments[-1][1]
        if latest_comments not in self.language_owner:
            self.bot_advice.append('new comment.')

    def multi_link_policy(self):
        if MULTI_LINK_LABEL in self.issue_package.labels_name:
            self.bot_advice.append('multi readme link!')

    def remind_logic(self) -> bool:
        return abs(self.date_from_target) <= 2

    def print_date_from_target_date(self) -> str:
        return str(self.date_from_target) if self.remind_logic() else ''

    def date_remind_policy(self):
        if self.remind_logic():
            self.bot_advice.append('close to release date. ')

    def auto_bot_advice(self):
        self.new_issue_policy()
        self.new_comment_policy()
        self.multi_link_policy()
        self.date_remind_policy()

    def get_target_date(self):
        body = self.get_issue_body()
        try:
            self.target_date = [line.split(':')[-1].strip() for line in body if 'Target release date' in line][0]
            self.date_from_target = int((time.mktime(time.strptime(self.target_date, '%Y-%m-%d')) - time.time()) / 3600 / 24)
        except Exception:
            self.target_date = 'fail to get.'
            self.date_from_target = 1000  # make a ridiculous data to remind failure when error happens

    def run(self) -> None:
        # common part(don't change the order)
        self.auto_assign()  # necessary flow
        self.auto_parse()  # necessary flow
        self.get_target_date()
        self.auto_bot_advice()  # make sure this is the last step


class Common:
    """ The class defines some function for all languages to reference
    issues_package = None  # issues that need to handle
    request_repo_dict = {}  # request repo instance generated by different token
    assignee_candidates = {}  # assignee candidates who will be assigned to handle issue
    language_owner = {}  # language owner who may handle issue
    result = []
    file_out_name = ''  # file that storages issue status
    """

    def __init__(self, issues_package: List[IssuePackage], assignee_token: Dict[str, str], language_owner: Set[str]):
        self.issues_package = issues_package
        self.assignee_candidates = set(assignee_token.keys())
        self.language_owner = language_owner
        # arguments add to language.md
        self.file_out_name = 'common.md'
        self.target_release_date = ''
        self.date_from_target = ''
        self.package_name = ''
        self.result = []
        self.request_repo_dict = {}

        for assignee in assignee_token:
            self.request_repo_dict[assignee] = Github(assignee_token[assignee]).get_repo(REQUEST_REPO)

    def output(self):
        with open(self.file_out_name, 'w') as file_out:
            file_out.write('| issue | author | package | assignee | bot advice | created date of issue | target release date | date from target |\n')
            file_out.write('| ------ | ------ | ------ | ------ | ------ | ------ | ------ | :-----: |\n')
            for item in self.result:
                try:
                    item_status = Common.output_md(item)
                    file_out.write(item_status)
                except Exception as e:
                    _LOG.error(f'Error happened during output result of handled issue {item.issue_package.issue.number}: {e}')

    @staticmethod
    def output_md(item: IssueProcess):
        create_date = str(date.fromtimestamp(item.issue_package.issue.created_at.timestamp()).strftime('%m-%d'))
        try:
            target_date = str(datetime.strptime(item.target_date, "%Y-%m-%d").strftime('%m-%d'))
        except:
            target_date = str(item.target_date)

        return '| [#{}]({}) | {} | {} | {} | {} | {} | {} | {} |\n'.format(
            item.issue_package.issue.html_url.split('/')[-1],
            item.issue_package.issue.html_url,
            item.issue_package.issue.user.login,
            item.package_name,
            item.assignee,
            ' '.join(item.bot_advice),
            create_date,
            target_date,
            item.print_date_from_target_date()
        )

    def run(self):
        items = []
        for item in self.issues_package:
            issue = IssueProcess(item, self.request_repo_dict, self.assignee_candidates, self.language_owner)
            try:
                issue.run()
                self.result.append(issue)
            except Exception as e:
                _LOG.error(f'Error happened during handling issue {item.issue.number}: {e}')
        self.output()


def common_process(issues: List[IssuePackage]):
    instance = Common(issues, _ASSIGNEE_TOKEN, _LANGUAGE_OWNER)
    instance.run()
