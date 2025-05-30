# Ansible Role: Homepage

This role deploys a customizable static HTML homepage. It can be configured with links to internal (intranet) and external (web) resources, grouped into categories.

## Requirements

- **Ansible:** Version 2.1 or higher.

- **User Variable:** The role tasks and default directory structure expect a variable named `user` to be defined, with the following attributes:

  - `user.name`: The username for file ownership.

  - `user.group`: The group for file ownership.

  - user.home: The home directory of the user (used in the default homepage_directory path).

        This variable should be provided in your playbook or inventory (e.g., as a host variable or group variable).

        Example:

    ```yaml
    user:
      name: "your_user"
      group: "your_group"
      home: "/home/your_user"
    ```

- **Template File:** The role attempts to use a Jinja2 template from `home/.local/share/html/homepage/index.html.j2` on the Ansible controller to generate the `index.html`. This is an unusual path. For a more portable role, you would typically place your `index.html.j2` inside the role's `templates/` directory and reference it as `src: index.html.j2`. The variables described below are intended to be used by such a template.

## Role Variables

The following variables can be set to customize the homepage. Default values are defined in `defaults/main.yml`.

### `homepage_directory`

- **Description:** The directory on the target server where the homepage files will be deployed.

- **Default:** `{{ user.home }}/.local/share/html/homepage`

- **Example:**

    ```yaml
    homepage_directory: "/var/www/myhomepage"
    ```

### `homepage_intranet_hosts`

- **Description:** A dictionary that maps short, friendly names to the IP addresses or hostnames of your internal services. This makes it easier to manage and reference intranet links within the `homepage_groups` variable. The generated `index.html` (via the template) will use these values to construct the actual URLs.

- **Default:**

    ```yaml
    homepage_intranet_hosts:
      hookerbot: 192.168.41.1
      crambot: crambot
      ninjabot: ninjabot
      localhost: localhost
    ```

- **How to customize:** Add or modify entries to reflect your network's services.

    ```yaml
    homepage_intranet_hosts:
      fileserver: 192.168.1.10
      wikiserver: "wiki.internal.corp"
      # Add other hosts from defaults if still needed
      localhost: localhost
    ```

### `homepage_groups`

- Description: This is the primary variable for defining the content of your homepage. It's a dictionary where each key represents a group/category of links (e.g., "Productivity Tools", "Development Resources"). The value for each key is a list of link definitions.

    There are two types of link definitions:

    1. **Intranet Links:** Used for services within your local network.

        - `name`: (Required) The display text for the link.

        - `host`: (Required) A key that must correspond to an entry in `homepage_intranet_hosts`.

        - `scheme`: (Optional) The URL scheme (e.g., `http`, `https`). Defaults to `http` if not specified by the template logic.

        - `port`: (Optional) The port number for the service. Defaults to `80` for `http` and `443` for `https` if not specified by the template logic.

        - `path`: (Optional) The path component of the URL (e.g., `/admin`, `/dashboard`). Defaults to `/` if not specified.

    2. **Web Links:** Used for external websites.

        - `name`: (Required) The display text for the link.

        - `url`: (Required) The full URL for the external link.

- **Default:** The `defaults/main.yml` file contains an extensive list of predefined groups and links for `intranet`, `intranetLLM`, `webtools`, `webtoolsmisc`, `webtoolsLLM`, and `webtoolsLLMchat`.

- **How to customize:** You can override this entire dictionary in your playbook or inventory variables to define your own link structure.

    ```yaml
    homepage_groups:
      my_services:
        - name: "Internal Wiki"
          host: "wikiserver" # Must be defined in homepage_intranet_hosts
          scheme: "https"
          path: "/main"
        - name: "File Share"
          host: "fileserver"
          port: 8080
      favorite_sites:
        - name: "Ansible Docs"
          url: "[https://docs.ansible.com/](https://docs.ansible.com/)"
        - name: "Tech News"
          url: "[https://news.ycombinator.com/](https://news.ycombinator.com/)"
    ```

## Dependencies

This role has no external Ansible Galaxy role dependencies.

## Tasks Overview

The role performs the following main tasks:

1. **Create Homepage Folder:** Ensures the `{{ homepage_directory }}` exists on the target host with the correct owner, group, and permissions.

2. **Sync Folder:** Synchronizes content from a source directory (`home/.local/share/html/homepage/` on the Ansible controller) to the `{{` homepage_directory }} on the target. This step seems intended to copy static assets like CSS, JavaScript, or images.

    - **Note:** The `src` path is unusual. Typically, role files are self-contained. You might want to place these assets in the role's `files/` directory and use the `ansible.builtin.copy` module.

3. **Set index.html Template:** Generates the `index.html` file in `{{ homepage_directory }}` using the `ansible.builtin.template` module.

    - **Source Template:** `home/.local/share/html/homepage/index.html.j2` (on the Ansible controller).

    - Destination: {{ homepage_directory }}/index.html

        This template is responsible for iterating through the homepage_groups and homepage_intranet_hosts variables to render the links.

## Example Playbook

Here's an example of how to use this role in a playbook:

```yaml
- hosts: webservers
  become: yes # Depending on homepage_directory permissions
  vars:
    user: # This user variable must be defined
      name: "www-data"
      group: "www-data"
      home: "/var/www" # Example, adjust as needed

    homepage_directory: "/var/www/custom_homepage" # Override default

    homepage_intranet_hosts:
      mainserver: "10.0.0.5"
      backupserver: "10.0.0.6"
      localhost: "127.0.0.1" # Always good to have

    homepage_groups:
      company_portals:
        - name: "HR Portal"
          host: "mainserver"
          scheme: "https"
          port: 8443
          path: "/hr"
        - name: "Backup System"
          host: "backupserver"
          port: 8000
      external_tools:
        - name: "Project Management"
          url: "[https://yourprojecttool.example.com](https://yourprojecttool.example.com)"
        - name: "Version Control"
          url: "[https://github.com/yourorg](https://github.com/yourorg)"

  roles:
    - role: homepage # Or your_username.homepage if from Galaxy
```

## Customizing the Homepage Appearance

- **Via Variables:** The primary way to customize the _content_ (links and groups) is by defining `homepage_intranet_hosts` and `homepage_groups`.

- **Via Template:** To change the HTML structure, layout, or styling significantly, you would need to modify or replace the source Jinja2 template (`home/.local/share/html/homepage/index.html.j2` on the controller, or preferably, a template within the role's `templates/` directory). The `index-alt.html` file provided in your role's `templates` directory appears to be a static HTML file; if you intend to use it as the base, it should be converted to a Jinja2 template (`.j2`) that utilizes the role variables.

- **Via Synced Files:** If the `synchronize` task is used to copy CSS, JavaScript, or image files, you can customize these files in the source directory (`home/.local/share/html/homepage/` on the controller) to alter the appearance.

## License

BSD (As per the original `meta/main.yml`, please update if different)

## Author Information

(Update with your information)
